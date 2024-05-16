from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth as auth2
from datetime import datetime

login_or_signup = Blueprint('login_or_signup', import_name=__name__, template_folder='templates')

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
cred = credentials.Certificate(r".\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Pyrebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

@login_or_signup.route('/loginorsignup')
def login_or_signup_home():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = db.child('Users').child(user_id).get().val()
        return render_template('logged.html', user=user_data)
    else:
       form_type = request.args.get('form', 'login')
       return render_template('login_or_signup.html', form_type=form_type)

@login_or_signup.route('/login', methods=['POST'])
def login():
    email = request.form['login_email']
    password = request.form['login_password']

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        user_id = user['localId']

        user_data = db.child('Users').child(user_id).get().val()
        if user_data is None:
            flash('Bu kullanıcı mevcut değil.', 'error')
            return redirect(url_for('login_or_signup.login_or_signup_home', form='login'))
        
        if user_data['password'] != password or user_data['email'] != email:
            flash('Giriş başarısız. Bilgilerinizi kontrol edin.', 'error')
            return redirect(url_for('login_or_signup.login_or_signup_home', form='login'))
                            
        session['user_id'] = user_id
        return redirect(url_for('login_or_signup.logged'))

    except Exception as e:
        error_message = str(e)
        print(f"Login failed: {error_message}")
        flash('Giriş başarısız. Bilgilerinizi kontrol edin.', 'error')
        return redirect(url_for('login_or_signup.login_or_signup_home', form='login'))

@login_or_signup.route('/signup', methods=['POST'])
def register():
    name = request.form['signup_name']
    surname = request.form['signup_surname']
    email = request.form['signup_email']
    password = request.form['signup_password_1']
    password_confirm = request.form['signup_password_2']

    if len(password) < 8 or password != password_confirm:
        if len(password) < 8:
            flash('Parola en az 8 karakter olmalıdır.', 'error')
        if password != password_confirm:
            flash('Parolalar eşleşmiyor.', 'error')
        return redirect(url_for('login_or_signup.login_or_signup_home', form='signup'))

    
    try:
        user = auth.create_user_with_email_and_password(email=email, password=password)
        user_id = user['localId']

        registration_date = datetime.now().strftime("%b %d, %Y at %H:%M:%S UTC+3")
        sub_types = ['Free', 'Basic', 'Advanced']

        sub_types_descriptions = ['Free paket sadece etkinlik yazısı oluşturur.',
                                  'Basic paket etkinlik yazısı ve görsel oluşturma içerir.',
                                  'Advanced paket etkinlik yazısı, görsel oluşturma ve Linkedin API entegrasyonu içerir.']
        
        sub_daily_rights = ['5','15','30']
 
        user_data = {
            'name': name,
            'surname': surname,
            'email': email,
            'password': password,
            'created_at': registration_date,
            'sub_type': sub_types[0],
            'daily_rights': 5,
            'expire_date': "none"
        }

        sub_data = {
            'description': sub_types_descriptions[0],
            'price': 0,
            'price_currency': 'TL',
            'sub_daily_rights': sub_daily_rights[0],
            'sub_name': sub_types[0]
        }

        db.child('Users').child(user_id).set(user_data)

        db.child('Subscriptions').child(sub_types[0]).set(sub_data)
        
        session['user_id'] = user_id
        return redirect(url_for('login_or_signup.logged'))
    
    except Exception as e:
        error_message = str(e)
        print(f"Registration failed: {error_message}")
        flash('Kullanıcı kaydı başarısız. Bu e-posta adresi zaten kullanılıyor.', 'error')
        return redirect(url_for('login_or_signup.login_or_signup_home', form='signup'))

@login_or_signup.route('/logged')
def logged():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = db.child('Users').child(user_id).get().val()
        return render_template('logged.html', user=user_data)
    else:
        return redirect(url_for('login_or_signup.login_or_signup_home'))

@login_or_signup.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = db.child('Users').child(user_id).get().val()
        return render_template('dashboard.html', user=user_data)
    else:
        return redirect(url_for('login_or_signup.login_or_signup_home'))
    
@login_or_signup.route('/reset_password', methods=['POST'])
def reset_password():
    if 'user_id' in session:
        user_id = session['user_id']
        new_password = request.form['new_password']
        try:
            user = auth2.update_user(user_id, password=new_password)
            db.child('Users').child(user_id).update({'password': new_password})
            flash('Password successfully changed.', 'success')
            return redirect(url_for('login_or_signup.dashboard'))
        except Exception as e:
            print(e)
            flash('Failed to change password.', 'error')
            return redirect(url_for('login_or_signup.dashboard'))
    else:
        return redirect(url_for('login_or_signup.login_or_signup_home'))
    
@login_or_signup.route('/change_email', methods=['POST'])
def change_email():
    if 'user_id' in session:
        user_id = session['user_id']
        new_email = request.form['new_email']
        try:
            user = auth2.update_user(user_id, email=new_email)
            db.child('Users').child(user_id).update({'email': new_email})
            flash('Email successfully changed.', 'success')
            return redirect(url_for('login_or_signup.dashboard'))
        except Exception as e:
            print(e)
            flash('Failed to change email.', 'error')
            return redirect(url_for('login_or_signup.dashboard'))
    else:
        return redirect(url_for('login_or_signup.login_or_signup_home'))

@login_or_signup.route('/logout')
def logout():
    auth.current_user = None
    session.clear()
    return redirect(url_for('login_or_signup.login_or_signup_home'))