from flask import Flask, render_template, redirect, url_for, session, request,flash
from datetime import datetime
import os
from models import fetch_data, add_to_collection, register, login_
from flask_bcrypt import Bcrypt
import sys

dir_name = os.path.dirname(__file__)
DATA_FILE = os.path.join(dir_name,'Data','data.json')
today = datetime.now().strftime('%Y-%m-%d')

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

@app.route('/auth_register',methods=['POST','GET'])
def auth_register():
    if request.method != 'POST':
        return redirect(url_for("sign_up"))
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    if password == confirm_password:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    if register(user=username,email=email,password=hashed_password,date=today):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/auth_login',methods=['GET','POST'])
def auth_login():
    if request.method != 'POST':
        return redirect(url_for("login"))
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        result = login_(email=email) 
        if result:
            username = result.get('username')
            pwd = result.get('password')
            if bcrypt.check_password_hash(pwd,password):
                print(result)
                session['user'] = username
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('index'))
    
@app.route('/add-item', methods=['POST'])
def add_item():
    transaction_date = request.form.get('transaction_date')
    transaction_type = request.form.get('type')
    transactions = request.form.get('transactions')
    amount = request.form.get('Amount')
    add_to_collection(date=transaction_date,description=transactions,amount=amount,type=transaction_type,user=session['user'])
    return redirect(url_for('dashboard'))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('index'))

@app.route('/login', methods = ['GET','POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'),name=session['user'])
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    rows = fetch_data(user=session['user'])
    return render_template('dashboard.html', today=today, name=session['user'],rows=rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
