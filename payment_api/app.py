from flask import Flask, request, jsonify
import os
from pymongo import MongoClient
import uuid

app = Flask(__name__)

# Configure MongoDB
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/paymentdb')
client = MongoClient(MONGO_URI)
db = client.paymentdb
payments_collection = db.payments

@app.route('/api/payments', methods=['POST'])
def create_payment():
    try:
        data = request.json
        if not data or 'amount' not in data or 'currency' not in data:
            return jsonify({'error': 'Invalid request. Amount and currency are required.'}), 400
        
        payment_id = str(uuid.uuid4())
        payment_record = {
            'payment_id': payment_id,
            'amount': data['amount'],
            'currency': data['currency'],
            'status': 'SUCCESS',
            'user': data.get('user', 'guest')
        }
        
        payments_collection.insert_one(payment_record)
        
        # Remove MongoDB object ID before returning
        payment_record.pop('_id', None)
        return jsonify({'message': 'Payment processed successfully', 'payment': payment_record}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/payments', methods=['GET'])
def get_payments():
    try:
        payments = list(payments_collection.find({}, {'_id': 0}))
        return jsonify({'payments': payments}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
