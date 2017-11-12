from flask import abort
from flask import json
from flask import jsonify
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from app import app
from app import qbo
from .intuit import BASE_URL, PURCHASE_OP, REDIRECT_URI_DEV
from .costco_regex import receipt_reader

import json
import requests


@app.route('/')
def index():
    return jsonify(**{ 'reply': 'Hello, World!'})

@app.route('/v1/application/processReceipt', methods=['GET', 'POST'])
def process_receipt():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('auth'))
    data = request.get_json()
    #if not data:
    #    return jsonify(**{'postData': 'No data'})
    #receipt_raw = data['content']
    # do some processing here
    #body = create_request_body(receipt_raw)
    # Now create a new purchase object to Quickbooks
    headers = {'Content-Type': 'application/json'}
    headers['Authorization'] = 'Bearer ' + access_token
    headers['Accept'] = 'application/json'
    #r = qbo.post(PURCHASE_OP, data={}, headers=headers)
    payload = json.dumps(receipt_reader())
    r = requests.post(BASE_URL + PURCHASE_OP, headers=headers, data=payload)
    return jsonify(**{
        'processStatus': 'Success',
        'data': r.text,
    })

@app.route('/auth')
def auth():
    return qbo.authorize(callback=url_for(REDIRECT_URI_DEV))

@app.route('/oauth_authorized')
@qbo.authorized_handler
def oauth_authorized(resp):
    if 'error' in request.args:
        return jsonify(**{
            'authStatus': 'Fail',
            'errorResp': request.args.get('error'),
        })
    if resp is None:
        return jsonify(**{'authStatus': 'Fail'})
    # Setting the session using flask session just for prototyping
    session['is_authorized'] = True
    session['access_token'] = resp.get('access_token')
    return jsonify(**{'authStatus': 'Success'})
