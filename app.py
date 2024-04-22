from flask import Flask, render_template, request, redirect, flash
from auth import *

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    if tryLogin(email, password) == "fail":
        flash('Invalid username or password', 'error')
        return redirect('/login_error')
    
    return "login successful"

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if trySignUp(email, password) == "fail":
            flash('Signup process failed', 'error')
            return redirect('/signup_error')
        
        return "Registration successful"
    
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to your dashboard!"

@app.route('/login_error')
def login_failed():
    return render_template('login_error.html')

@app.route('/signup_email_used')
def signup_email_used():
    return render_template('signup_email_used.html')

@app.route('/signup_error')
def signup_failed():
    return render_template('signup_error.html')

if __name__ == '__main__':
    app.secret_key = 'CS4440'
    app.run(debug=True)
