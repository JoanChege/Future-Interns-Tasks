from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client.jstar_designer

# Home Page
@app.route('/')
def index():
    categories = list(db.categories.find())
    return render_template('index.html', categories=categories)

# Product Listings
@app.route('/product/<category>')
def product(category):
    products = list(db.products.find({"category": category}))
    return render_template('product.html', products=products, category=category)

# Cart
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

# Add to Cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    product_id = request.form.get('product_id')
    product = db.products.find_one({"_id": ObjectId(product_id)})
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product)
    session.modified = True
    return redirect(url_for('cart'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.users.find_one({"email": email, "password": password})
        if user:
            session['user'] = user['email']
            return redirect(url_for('index'))
        else:
            return "Invalid login credentials"
    return render_template('login.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        db.users.insert_one({"email": email, "password": password})
        return redirect(url_for('login'))
    return render_template('register.html')

# Checkout
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)
