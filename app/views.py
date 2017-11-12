from flask import abort
from flask import json
from flask import jsonify
from flask import request
from app import app

@app.route('/')
def index():
    return jsonify(**{ 'reply': 'Hello, World!'})

@app.route('/v1/application/processReceipt', methods=['POST'])
def process_receipt():
    data = request.get_json()
    receipt_raw = data['content']
    print(receipt_raw)
