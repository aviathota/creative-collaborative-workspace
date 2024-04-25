from flask import Flask, render_template, request, redirect, flash
from auth import *
import db_secrets as sec
import data as dt

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
    
    dt.userData['email'] = email
    return render_template('profile.html', profile=dt.retrieveUserData(dt.userData['email']))

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if trySignUp(email, password) == "fail":
            flash('Signup process failed', 'error')
            return redirect('/signup_error')
        
        dt.userData['email'] = email
        dt.createUser(dt.userData['email'])
        return render_template('profile.html', profile=dt.retrieveUserData(dt.userData['email']))
    
    return render_template('signup.html')

@app.route('/login_error')
def login_failed():
    return render_template('login_error.html')

@app.route('/signup_email_used')
def signup_email_used():
    return render_template('signup_email_used.html')

@app.route('/signup_error')
def signup_failed():
    return render_template('signup_error.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', profile=dt.retrieveUserData(dt.userData['email']))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    try:
        data = request.json
        dt.updateUser(dt.userData['email'], data['name'], data['age'], data['location'], data['birthday'], data['summary'])
        return "success"
    except:
        return "fail"

if __name__ == '__main__':
    dt.userData = {}
    app.secret_key = sec.firebase_secret_key
    app.run(debug=True)
