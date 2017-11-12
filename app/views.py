from flask import abort
from flask import json
from flask import jsonify
from flask import session
from flask import url_for
from app import app
from app import qbo
from .intuit import PURCHASE_OP

@app.route('/')
def index():
    return jsonify(**{ 'reply': 'Hello, World!'})

@app.route('/v1/application/processReceipt', methods=['GET', 'POST'])
def process_receipt():
    data = request.get_json()
    if not data:
        return jsonify(**{'postData': 'No data'})
    receipt_raw = data['content']
    # do some processing here
    body = create_request_body(receipt_raw)
    # Now create a new purchase object to Quickbooks
    headers = {'Content-Type': 'application/json'}
    r = qbo.post(PURCHASE_OP, data={}, headers=headers)

@app.route('/auth')
def auth():
    return qbo.authorize(callback=url_for('oauth_authorized'))

@app.route('/oauth-authorized')
@qbo.authorized_handler
def oauth_authorized(resp):
    if 'error' in request.args:
        return jsonify(**{
            'authStatus': 'Fail',
            'errorResp': request.args.get('error'),
        })
    realm_id = str(request.args.get('realmId'))
    state = str(request.args.get('state'))
    code = str(request.args.get('code'))
    print(code)
    if resp is None or state is not 'MERDE':
        print('You denied the request to sign in.')
        return jsonify(**{'authStatus': 'Fail'})
    # Setting the session using flask session just for prototyping
    session['is_authorized'] = True
    session['realm_id'] = realm_id
