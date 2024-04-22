import pyrebase
import app

config = {
    'apiKey': "AIzaSyCWaWRquF1FDSetC25OYvt3WrT4dXXfO7s",
    'authDomain': "ccw-auth.firebaseapp.com",
    'projectId': "ccw-auth",
    'storageBucket': "ccw-auth.appspot.com",
    'messagingSenderId': "828962097424",
    'appId': "1:828962097424:web:f2c19b0e334318bcd0fd95",
    'measurementId': "G-6WLZ3G3S5J",
    'databaseURL': ""
}

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
