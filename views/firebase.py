from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth as auth2

firebase_app = Blueprint('firebase_app', import_name=__name__, template_folder='templates')

config = {
    'apiKey': 'AIzaSyCJLY7X-mX6iOmOK8XufMHdw6njfLvJeEw',
    'authDomain': 'eventosphere-26942.firebaseapp.com',
    'databaseURL': 'https://eventosphere-26942-default-rtdb.firebaseio.com/',
    'projectId': 'eventosphere-26942',
    'storageBucket': 'eventosphere-26942.appspot.com',
    'messagingSenderId': '967596452041',
    'appId': '1:967596452041:web:ddf8362d3e2a013f08c518'
}

# Firebase Admin
cred = credentials.Certificate(r"C:\Users\CAGRII\Desktop\Firebase Flask\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Pyrebase
firebase = pyrebase.initialize_app(config)
auth= firebase.auth()
db=firebase.database()

@firebase_app.route('/firebase')
def firebase_home():
    return render_template('loginorsignup.html')

def get_user_data(user_id):
    db = firebase.database()
    user_data = db.child('users').child(user_id).get().val()
    return user_data

@firebase_app.route('/login', methods=['POST'])
def login():
    email = request.form['login_email']
    password = request.form['login_password']

    try:
        # Firebase Authentication kullanarak kullanıcıyı giriş yap
        user = auth.sign_in_with_email_and_password(email, password)
        user_id = user['localId']
        session['user_id'] = user_id

        return redirect(url_for('firebase_app.dashboard'))

    except Exception as e:
        print(e)
        return "Login failed."

@firebase_app.route('/signup', methods=['POST'])
def register():
    username = request.form['signup_username']
    name = request.form['signup_name']
    surname = request.form['signup_surname']
    email = request.form['signup_email']
    password = request.form['signup_password']
    
    if len(password) < 8:
        return render_template('loginorsignup.html', message="Password must be at least 8 characters long.")
    
    try:
        # Firebase Authentication kullanarak kullanıcı kaydı yap
        user = auth.create_user_with_email_and_password(email=email, password=password)
        user_id = user['localId']
        
        # Firebase Realtime Database'e kullanıcıyı kaydet
        data = {
            'username': username,
            'name': name,
            'surname': surname,
            'email': email,
            'password': password
        }
        db.child('users').child(user_id).set(data)
        
        session['user_id'] = user_id
        return redirect(url_for('firebase_app.dashboard'))
    
    except Exception as e:
        print(e)
        return "User registration failed."
        

@firebase_app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = db.child('users').child(user_id).get().val()
        return render_template('dashboard.html', user=user_data)
    else:
        return redirect(url_for('firebase_app.firebase_home'))

@firebase_app.route('/reset_password', methods=['POST'])
def reset_password():
    if 'user_id' in session:
        user_id = session['user_id']
        new_password = request.form['new_password']
        try:
            user = auth2.update_user(user_id, password=new_password)
            db.child('users').child(user_id).update({'password': new_password})
            flash('Password successfully changed.', 'success')
            return redirect(url_for('firebase_app.dashboard'))
        except Exception as e:
            print(e)
            flash('Failed to change password.', 'error')
            return redirect(url_for('firebase_app.dashboard'))
    else:
        return redirect(url_for('riebase_app.firebase_home'))
    
@firebase_app.route('/change_email', methods=['POST'])
def change_email():
    if 'user_id' in session:
        user_id = session['user_id']
        new_email = request.form['new_email']
        try:
            user = auth2.update_user(user_id, email=new_email)
            db.child('users').child(user_id).update({'email': new_email})
            flash('Email successfully changed.', 'success')
            return redirect(url_for('firebase_app.dashboard'))
        except Exception as e:
            print(e)
            flash('Failed to change email.', 'error')
            return redirect(url_for('firebase_app.dashboard'))
    else:
        return redirect(url_for('firebase_app.firebase_home'))

@firebase_app.route('/logout', methods=['POST'])
def logout():
    auth.current_user = None
    session.clear()
    return redirect(url_for('firebase_app.firebase_home'))

