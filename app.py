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

@app.route('/projects')
def projects():
    return render_template('projects.html', profile=dt.retrieveUserData(dt.userData['email']))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    try:
        data = request.json
        dt.updateUser(dt.userData['email'], data['name'], data['age'], data['location'], data['birthday'], data['summary'])
        return "success"
    except:
        return "fail"

@app.route('/messages')
def messages():
    return render_template('messages.html', profile=dt.retrieveUserData(dt.userData['email']))

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.json
        dt.createMessage(dt.userData['email'], data['receiver'], data['message'])
        return "success"
    except:
        return "fail"

@app.route('/fetch_messages')
def messages_page():
    messages = dt.fetchMessages(dt.userData['email'])
    return render_template('fetch_messages.html', messages=messages)

@app.route('/create_project', methods=['POST'])
def create_project():
    try:
        data = request.json
        project_name = data.get('projectName')
        contributors = data.get('contributors')
        response = dt.createNewProject(project_name, dt.userData['email'])
        response = dt.inviteMembers(project_name, contributors)
        return "success"
    except:
        return "fail"    

@app.route('/view_projects')
def view_projects():
    projects = dt.getProjectsWithUser(dt.userData['email'])
    return render_template('view_projects.html', projects=projects)

@app.route('/project/<project_name>')
def project(project_name):
    if dt.checkProjectPerms(dt.userData['email'], project_name) == "success":
        project_info = dt.getProjectInfo(project_name)
        return render_template('project.html', project=project_info)
    else:
        return render_template('invalid_perms.html')

@app.route('/invalid_perms')
def invalid_perms():
    return render_template('invalid_perms.html')

if __name__ == '__main__':
    dt.userData = {}
    app.secret_key = sec.firebase_secret_key
    app.run(debug=True)
