from flask import abort
from flask import json
from flask import jsonify
from flask import request
from app import app

@app.route('/')
def index():
    return jsonify(**{ 'reply': 'Hello, World!'})

@app.route('/v1/application/processReceipt', methods=['GET', 'POST'])
def process_receipt():
    data = request.get_json()
    if not data:
        return jsonify(**{'postData': 'No data'})
    receipt_raw = data['content']
    return jsonify(**{ 'postData': receipt_raw })
