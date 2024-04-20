from flask import Flask, render_template, request, redirect, flash
from auth import *

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if tryLogin(username, password) != 1:
        return "login fail lol"
        return redirect('/')
    
    return redirect('/dashboard')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

if __name__ == '__main__':
    app.secret_key = 'secret key'
    app.run(debug=True)
