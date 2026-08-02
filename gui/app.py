from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

PAYMENT_API_URL = os.getenv('PAYMENT_API_URL', 'http://localhost:8080/api/payments')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        amount = request.form.get('amount')
        currency = request.form.get('currency')
        user = request.form.get('user', 'Guest')
        
        payload = {
            'amount': float(amount) if amount else 0.0,
            'currency': currency,
            'user': user
        }
        
        try:
            response = requests.post(PAYMENT_API_URL, json=payload, timeout=5)
            if response.status_code == 201:
                flash('Payment successful!', 'success')
            else:
                flash(f"Payment failed: {response.json().get('error', 'Unknown error')}", 'danger')
        except requests.exceptions.RequestException as e:
            flash(f"Could not connect to payment service: {str(e)}", 'danger')
            
        return redirect(url_for('index'))
        
    # GET request: fetch transaction history
    transactions = []
    try:
        resp = requests.get(PAYMENT_API_URL, timeout=5)
        if resp.status_code == 200:
            transactions = resp.json().get('payments', [])
    except Exception as e:
        flash(f"Warning: Could not fetch transaction history: {str(e)}", 'warning')

    return render_template('index.html', transactions=transactions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
