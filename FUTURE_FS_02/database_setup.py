from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['jstar_designer']

# Insert categories
categories = [
    {"name": "Dresses", "image": "dresses.jpg"},
    {"name": "Pant and Dress Suits", "image": "suits.jpg"},
    {"name": "Shirt Dress", "image": "shirtdress.jpg"},
    {"name": "Coats", "image": "coats.jpg"},
    {"name": "Shoes and Panties", "image": "shoes.jpg"}
]

db.categories.drop()  # Clear existing data
db.categories.insert_many(categories)

# Insert sample products
products = [
    {"name": "Red Evening Dress", "category": "Dresses", "price": 4500, "image": "reddress.jpg"},
    {"name": "Blue Office Suit", "category": "Pant and Dress Suits", "price": 5000, "image": "blacksuit.jpg"},
    {"name": "Casual Shirt Dress", "category": "Shirt Dress", "price": 3000, "image": "blueshirtdress.jpg"},
    {"name": "Winter Long Coat", "category": "Coats", "price": 8000, "image": "coat.jpg"},
    {"name": "Stylish Heels", "category": "Shoes and Panties", "price": 3500, "image": "heels.jpg"}
]

db.products.drop()  # Clear existing data
db.products.insert_many(products)

# Insert a sample user (hashed password for security)
from werkzeug.security import generate_password_hash

users = [
    {"email": "testuser@example.com", "password": generate_password_hash("password123")}
]

db.users.drop()  # Clear existing data
db.users.insert_many(users)

print("Database setup completed!")
