from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'your_paco_key_is_here'  # Set a secure key for session handling

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
    product = db.products.find_one({"_id": ObjectId(product_id)})  # Find product in MongoDB by its ID
    if 'cart' not in session:  # Initialize the cart if it's not already in session
        session['cart'] = []
    session['cart'].append(product)  # Add product to the cart
    session.modified = True  # Mark the session as modified
    return redirect(url_for('cart'))  # Redirect to the cart page

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
