import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
import razorpay
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Replace these with your actual Razorpay API Keys or use a .env file
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_YOUR_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "YOUR_KEY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Pricing dictionary mapped to Plan IDs (Prices in INR)
PLANS = {
    "monthly": {"name": "Monthly Elite", "amount": 1999},
    "quarterly": {"name": "Quarterly Pro", "amount": 4999},
    "annual": {"name": "Annual Champion", "amount": 14999}
}

@app.route('/')
def index():
    return render_template('index.html', razorpay_key_id=RAZORPAY_KEY_ID, plans=PLANS)

@app.route('/create-order', methods=['POST'])
def create_order():
    try:
        data = request.json
        plan_id = data.get('plan_id')
        
        if plan_id not in PLANS:
            return jsonify({"error": "Invalid plan selected"}), 400
            
        plan = PLANS[plan_id]
        # Razorpay accepts amounts in paise (1 INR = 100 paise)
        amount_in_paise = plan['amount'] * 100
        
        order_data = {
            "amount": amount_in_paise,
            "currency": "INR",
            "receipt": f"receipt_{plan_id}",
            "payment_capture": 1 # Auto capture payment
        }
        
        order = client.order.create(data=order_data)
        return jsonify(order)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verify-payment', methods=['POST'])
def verify_payment():
    try:
        payment_id = request.form.get('razorpay_payment_id')
        order_id = request.form.get('razorpay_order_id')
        signature = request.form.get('razorpay_signature')
        
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        # Verifies the payment signature authenticity
        client.utility.verify_payment_signature(params_dict)
        return redirect(url_for('payment_success', payment_id=payment_id))
    except Exception as e:
        return redirect(url_for('payment_failed'))

@app.route('/success')
def payment_success():
    payment_id = request.args.get('payment_id', '')
    return render_template('success.html', payment_id=payment_id)

@app.route('/failed')
def payment_failed():
    return render_template('failed.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
