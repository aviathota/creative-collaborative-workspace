import pyrebase
import app
import db_secrets as sec

config = sec.config

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def tryLogin(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return "success"
    except:
        return "fail"

def trySignUp(email, password):
    try:
        auth.create_user_with_email_and_password(email, password)
        return "success"
    except:
        return "fail"
