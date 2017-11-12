from flask import abort
from flask import json
from flask import jsonify
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask_cors import cross_origin
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
        access_token = 'eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..1E_gC9bC9jNzBJ09v71qbg.QsMWo85H_O8pPrXZz6BzCmrJMIIYye0DfOa0OuYmd1pInNh2j0DwmvxzG_OmbU8zl0vboQLmihzaGj5qtzxBlzs2U0qu3iLYTRH1VnJVm8Xgk_OAP0tPxbeC3j51-7DOt93W0jKriuG0q7UkjAYI5W0_SZ42hsf2-n49Gj1LziXMTquHLRnlpKzg11YFtYWMZ-Q_4KqTDN-12TRhFLReAMwmN3Pj6hoUwxjv9lr1S7kA7UIdnodOUj0-vY6gxDDZ3cv_myFJMNEYcfn2y007_2opCp5-nuDucq_bv09zkg1b9NPYjJvePKO_IQlSN2PA6RUHm-DrsKv3hz4XAROyBc6DAROgPmWOY1ZS7_tterG8-BIP6Wb5B7xUUW2iDpiJdpAUzIZq1KXncB4MQPQ_j6Bl0KntGDIGF2r_3fJ4ah7E_xieD6kQRCB8tMzFUZzPugsy-6qpWW5MayPZdbKBvvQ-qKQ5-y3IeFLO4rDbYRe3h9T6KinbPpEh9vgV8qyvn5juMgdc6JPQvm9ZCiSH8NKtIrzCScipZjx6u4gtxRNkWrWi0DiXlf0cOBpSAfwrl79QQFBuYPbgDmjVwzBEiZsHn_zwFba9RibQnORGIWouJPdIV78XVK52EMs-wJEfr5mcJrGNCHhg7f8mKXJdklckQad5wxyiMWh2V-G4AXVWyex5SQ1NjCas5MKnKLs0.FxIq523A8NYi3iNtB5DW5A'
    data = request.get_json()
    if not data:
        return jsonify(**{'postData': 'No data'})
    receipt_raw = data['content']
    # do some processing here
    # Now create a new purchase object to Quickbooks
    headers = {'Content-Type': 'application/json'}
    headers['Authorization'] = 'Bearer ' + access_token
    headers['Accept'] = 'application/json'
    #r = qbo.post(PURCHASE_OP, data={}, headers=headers)
    payload = json.dumps(receipt_reader(receipt_raw))
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
