from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.jstar_designer

# Insert categories
categories = [
    {"name": "Dresses", "image": "dresses.jpg"},
    {"name": "Pant and Dress Suits", "image": "suits.jpg"},
    {"name": "Shirt Dress", "image": "shirtdress.jpg"},
    {"name": "Coats", "image": "coats.jpg"},
    {"name": "Shoes and Panties", "image": "shoes.jpg"},
]
db.categories.insert_many(categories)

# Insert products
products = [
    {"name": "Red Dress", "price": 5000, "category": "Dresses", "image": "reddress.jpg"},
    {"name": "Black Suit", "price": 10000, "category": "Pant and Dress Suits", "image": "blacksuit.jpg"},
    {"name": "Blue Shirt Dress", "price": 6000, "category": "Shirt Dress", "image": "blueshirtdress.jpg"},
]
db.products.insert_many(products)
