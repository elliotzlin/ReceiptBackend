from flask import abort
from flask import json
from flask import jsonify
from flask import request
from flask import session
from flask import url_for
from app import app
from app import qbo
from .intuit import BASE_URL, PURCHASE_OP, REDIRECT_URI_PROD
from .costco_regex import receipt_reader

import json
import requests

@app.route('/')
def index():
    return jsonify(**{ 'reply': 'Hello, World!'})

@app.route('/v1/application/processReceipt', methods=['GET', 'POST'])
def process_receipt():
    data = request.get_json()
    #if not data:
    #    return jsonify(**{'postData': 'No data'})
    #receipt_raw = data['content']
    # do some processing here
    #body = create_request_body(receipt_raw)
    # Now create a new purchase object to Quickbooks
    headers = {'Content-Type': 'application/json'}
    headers['Authorization'] = 'Bearer eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0.._v9eWtvSGfTAE12wRyLEfw.5X5c9fK4N-gRnR_45t08gVDdBnoyqOR5gb-O6_IuQ5PRgwOAVE7TMbIu2EaZZfzWAtqzdeWG0Y8wPpJYoLCXwD8xY63pUvuf0LKMwRW3K-9jCsEsbiMY4UKSk_QdbBG8zbIsAMSpE7d9m8wdVu8TJVxcAl2ouZt29xGnAQnn-VSWQWEFAkv4P0UGvo9tVGcDiROxMCudA3kpFRCnqBl0ECmNs2jCwLl5FVjKrNKPJL6hUJEGIXPpIaYH7zeuJZQ9ixH_IwkkosYbufo1yalZ5G_G22XyFIifl5jpXIrLfSOFRJU1ddyX20Q4pwcBiS2vqZGbKB89-S0E84ph2G19f4kzI7Q_VkSVz7ON_JZ5gqXF-9qywwrxv3YkWMj0RE1bIlw_2UJpTCxdkQZ1z1mDKnTVtXmrvg9DD-wpCSjlzDpsQ1zleyn6joSvzSYq4Sxx5Jr_MDigxnVZLDKKjXffOWnSRfxshjVyMgLro-43JXBiihplpfBfRtMUwyAuKoirL32hIpcv-2DfxqTx1S1PyOWlihvPF4PO72AoogAugdR02fVTkForMMnUbPyFpp0hueRgNpaHXk5eHHCc1Dgf24fsOK3XerAB1A2XEAoDmbCjK6tcwgIamTLUkxkbcn9vASExRCdsLaX6USfVgk8SI78cc70YFqCv14AlgTEklPJek99Qirj_lmJKny2ilIsZ.wRqo8S9C-nYLpszygDsgbw'
    #r = qbo.post(PURCHASE_OP, data={}, headers=headers)
    payload = json.dumps(receipt_reader())
    r = requests.post(BASE_URL + PURCHASE_OP, headers=headers, data=payload)
    print(r.json())
    return r.json()

@app.route('/auth')
def auth():
    return qbo.authorize(callback=url_for(REDIRECT_URI_PROD))

@app.route('/oauth_authorized')
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
