from flask import Flask, render_template, request, redirect, url_for, session, jsonify
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
    try:
        product = db.products.find_one({"_id": ObjectId(product_id)})  # Find product by ObjectId
        if not product:
            return "Product not found", 404  # Handle case if product is not found

        # Convert ObjectId to string before storing it in the session
        product['_id'] = str(product['_id'])  # This converts the ObjectId to string

        # Initialize the cart if it doesn't exist in the session
        if 'cart' not in session:
            session['cart'] = []
            
        # Check if the product is already in the cart
        for item in session['cart']:
            if item['_id'] == product['_id']:
                item['quantity'] += 1  # If product exists, increase the quantity
                session.modified = True
                return redirect(url_for('cart'))

        product['quantity'] = 1
        session['cart'].append(product)  # Add the product to the cart
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

# Checkout Route
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')  # Render the checkout page

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
