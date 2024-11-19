from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_mail import Mail, Message
import requests
from pymongo import MongoClient
from bson.objectid import ObjectId
import json


# Custom JSON encoder for handling ObjectId serialization
class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super().default(obj)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_paco_key_is_here'  # Set a secure key for session handling
app.json_encoder = CustomJsonEncoder  # Use custom JSON encoder

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'
mail = Mail(app)


# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Connect to MongoDB
db = client.jstar_designer  # Access the 'jstar_designer' database

# Home Page Route
@app.route('/')
def index():
    categories = list(db.categories.find())  # Fetch all categories from MongoDB
    return render_template('index.html', categories=categories)  # Render home page with categories

# Product Listings Route
@app.route('/product/<category>')
def product(category):
    products = list(db.products.find({"category": category}))  # Fetch products based on category
    return render_template('product.html', products=products, category=category)  # Render the products page

# Cart Route
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])  # Retrieve cart items from session
    return render_template('cart.html', cart_items=cart_items)  # Render cart page

# Add to Cart Route
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')  # Get product ID from form
    size = request.form.get('size')  # Get size from form
    type_ = request.form.get('type')  # Get type from form

    try:
        # Find product by ObjectId
        product = db.products.find_one({"_id": ObjectId(product_id)})
        if not product:
            return "Product not found", 404  # Handle case if product is not found



        # Convert ObjectId to string before storing it in the session
        product['_id'] = str(product['_id'])  # Convert ObjectId to string

        # Initialize the cart if it doesn't exist in the session
        if 'cart' not in session:
            session['cart'] = []

        # Check if the product with the same size and type is already in the cart
        for item in session['cart']:
            if item['_id'] == product['_id'] and item.get('size') == size and item.get('type') == type_:
                item['quantity'] += 1  # If product exists with same size/type, increase the quantity
                session.modified = True
                return redirect(url_for('cart'))

        # Add size, type, and quantity to the product data
        product['size'] = size
        product['type'] = type_
        product['quantity'] = 1

        # Add the product to the cart
        session['cart'].append(product)
        session.modified = True  # Mark the session as modified

        return redirect(url_for('cart'))  # Redirect to the cart page

    except Exception as e:
        return f"Error: {str(e)}", 500  # Error handling for invalid ObjectId or database errors

# Remove from Cart Route
@app.route('/remove_from_cart/<product_id>')
def remove_from_cart(product_id):
    try:
        # Remove product by matching the ObjectId in the cart
        session['cart'] = [item for item in session['cart'] if item['_id'] != product_id]
        session.modified = True  # Mark the session as modified
        return redirect(url_for('cart'))  # Redirect to the cart page
    except Exception as e:
        return f"Error: {str(e)}", 500  # Handle any potential errors

# Decrease Quantity Route
@app.route('/decrease_quantity/<product_id>')
def decrease_quantity(product_id):
    try:
        # Find product in the cart
        for item in session['cart']:
            if item['_id'] == product_id:
                if item['quantity'] > 1:
                    item['quantity'] -= 1  # Decrease the quantity
                else:
                    session['cart'] = [cart_item for cart_item in session['cart'] if cart_item['_id'] != product_id]  # Remove item if quantity is 1
                session.modified = True  # Mark the session as modified
                break
        return redirect(url_for('cart'))  # Redirect to the cart page
    except Exception as e:
        return f"Error: {str(e)}", 500  # Handle any potential errors
    
# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # If the request method is POST (form submission)
        email = request.form.get('email')  # Get email from form
        password = request.form.get('password')  # Get password from form
        user = db.users.find_one({"email": email, "password": password})  # Check if user exists
        if user:
            session['user'] = user['email']  # Store user email in session
            return redirect(url_for('index'))  # Redirect to the home page
        else:
            return "Invalid login credentials"  # If credentials are incorrect
    return render_template('login.html')  # Render login page if it's a GET request

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # If the request method is POST (form submission)
        email = request.form.get('email')  # Get email from form
        password = request.form.get('password')  # Get password from form
        db.users.insert_one({"email": email, "password": password})  # Insert new user into the users collection
        return redirect(url_for('login'))  # Redirect to login page after registration
    return render_template('register.html')  # Render register page if it's a GET request

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    return render_template('checkout.html')

@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    payment_method = request.form.get('payment_method')
    user_email = 'user_email@example.com'  # Replace with the logged-in user's email

    if payment_method == 'visa':
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        # Mock Visa payment processing (use an actual payment gateway in production)
        if card_number and expiry_date and cvv:
            flash('Payment successful via Visa!', 'success')
            send_receipt(user_email)
        else:
            flash('Payment failed. Please check your Visa details.', 'danger')

    elif payment_method == 'mpesa':
        phone = request.form.get('phone')
        # Mock M-Pesa payment processing
        if phone:
            # Simulate sending payment prompt (API call to Safaricom)
            response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', json={
                'BusinessShortCode': '174379',
                'Password': 'your_encoded_password',
                'Timestamp': '20240101120000',
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': '1',  # Mock amount
                'PartyA': phone,
                'PartyB': '174379',
                'PhoneNumber': phone,
                'CallBackURL': 'https://yourdomain.com/callback',
                'AccountReference': 'JSTAR Designers',
                'TransactionDesc': 'Payment'
            }, headers={'Authorization': 'Bearer your_access_token'})
            if response.status_code == 200:
                flash('Payment prompt sent via M-Pesa!', 'success')
                send_receipt(user_email)
            else:
                flash('Payment failed. Please check your phone number.', 'danger')
        else:
            flash('Phone number is required for M-Pesa payment.', 'danger')

    return redirect(url_for('checkout'))

def send_receipt(email):
    msg = Message('Payment Receipt', sender='your_email@gmail.com', recipients=[email])
    msg.body = 'Thank you for your payment! Your order is confirmed.'
    mail.send(msg)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
