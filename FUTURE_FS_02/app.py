from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.secret_key = "joan_jstar_steve_key"  # Secret key for flash messages

# MongoDB setup
client = MongoClient("mongodb://localhost:27017")
db = client['JStarDesigner']
users = db['users']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["c_password"]

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for("register"))

        # Check if email or username already exists
        if users.find_one({"email": email}):
            flash("An account with this email already exists.")
            return redirect(url_for("register"))
        if users.find_one({"username": username}):
            flash("Username already taken. Please choose another one.")
            return redirect(url_for("register"))

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the database
        users.insert_one({"email": email, "username": username, "password": hashed_password})
        
        flash("Registration successful! You can now log in.")
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Find user by username
        user = users.find_one({"username": username})

        # Validate password
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            flash("Login successful!")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password. Please try again.")
            return redirect(url_for("login"))

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
