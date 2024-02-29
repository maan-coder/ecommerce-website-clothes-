from flask import Flask, render_template, request, session, redirect, url_for
import hashlib
from session18b import MongoDBHelper  # Assuming session18b is the correct module
from pymongo import MongoClient

web_app = Flask("Woolen Wear Clothes")
web_app.secret_key = 'woolenwearapp-key-1'  # Set secret_key for session

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')  # Update the connection string with your MongoDB URL
db = client['maans_collection']
orders_collection = db['orders']

@web_app.route("/")
def login_page():
    return render_template('home.html')

@web_app.route("/home")
def home():
    if 'login_username' in session:
        return render_template('login.html', email=session['login_username'], name=session['login_username'])
    else:
        return render_template('login.html')  # or redirect to login page

@web_app.route('/buy_now_men')
def buy_now_men():
    # Add logic to handle the "Buy Now" functionality for Men's Collection
    return render_template('buy_now_men.html')

@web_app.route('/buy_now_women')
def buy_now_women():
    # Add logic to handle the "Buy Now" functionality for Women's Collection
    return render_template('buy_now_women.html')


@web_app.route('/buy_now_kids')
def buy_now_kids():
    # Add logic to handle the "Buy Now" functionality for Women's Collection
    return render_template('buy_now_kids.html')


@web_app.route('/payment_page')
def payment_page():
    # Add logic for the payment page
    return render_template('payment_page.html')


# Add similar routes for other product categories

@web_app.route('/login', methods=['POST'])
def login():
    login_data = {
        'username': request.form['username'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
    }

    db = MongoDBHelper(collection="login")
    documents = db.fetch(login_data)

    if len(documents) >= 1:
        session['login_username'] = documents[0]['username']
        session['login_password'] = documents[0]['password']
        return render_template('home.html', email=session['login_username'], name=session['login_username'])
    else:
        return render_template('buy_now_women.html')

@web_app.route('/process_order', methods=['POST'])
def process_order():
    global orders_collection

    product = request.form.get('product')
    quantity = int(request.form.get('quantity'))
    name = request.form.get('name')
    email = request.form.get('email')

    print("Product:", product)
    print("Quantity:", quantity)
    print("Name:", name)
    print("Email:", email)
    return redirect(url_for('payment_page'))

def main():
    web_app.run(port=5050)

if __name__ == "__main__":
    main()