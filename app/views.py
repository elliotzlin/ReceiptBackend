from flask import abort
from flask import json
from flask import jsonify
from app import app
from app import qbo
from .intuit import PURCHASE_OP

import requests

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
