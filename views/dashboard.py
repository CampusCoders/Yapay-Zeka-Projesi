from flask import Flask, request, jsonify, render_template, Blueprint, session, url_for, redirect, flash
from views.loginorsignup import db, auth2, auth

dashboard = Blueprint('dashboard',import_name=__name__, template_folder='templates')

@dashboard.route('/dashboard')
def user_dashboard():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = db.child('Users').child(user_id).get().val()
        return render_template('dashboard.html', user=user_data)
    else:
        return redirect(url_for('login_or_signup.login_or_signup_home'))
    
@dashboard.route('/change_password', methods=['POST'])
def reset_password():
    if 'user_id' in session:
        user_id = session['user_id']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        try:
            if old_password == new_password:
                flash('Eski parolanız ve yeni parolanız aynı olamaz!','error')
                return redirect(url_for('dashboard.user_dashboard'))

            user_data = db.child('Users').child(user_id).get().val()
            if user_data['password'] != old_password:
                flash('Şuan kullandığınız parolanız doğru değil!', 'error')
                return redirect(url_for('dashboard.user_dashboard'))
            
            user = auth2.update_user(user_id, password=new_password)
            db.child('Users').child(user_id).update({'password': new_password})
            flash('Password successfully changed.', 'success')
            return redirect(url_for('dashboard.user_dashboard'))
        
        except Exception as e:
            print(e)
            flash('Failed to change password.', 'error')
            return redirect(url_for('dashboard.user_dashboard'))
    else:
        return redirect(url_for('login_or_signup.login_or_signup_home'))
    
@dashboard.route('/change_email', methods=['POST'])
def change_email():
    if 'user_id' in session:
        user_id = session['user_id']
        new_email = request.form['new_email']
        try:
            user = auth2.update_user(user_id, email=new_email)
            db.child('Users').child(user_id).update({'email': new_email})
            flash('Email successfully changed.', 'success')
            return redirect(url_for('dashboard.user_dashboard'))
        except Exception as e:
            print(e)
            flash('Failed to change email.', 'error')
            return redirect(url_for('dashboard.user_dashboard'))
    else:
        return redirect(url_for('login_or_signup.login_or_signup_home'))
    
@dashboard.route('/delete_user', methods=['POST'])
def delete_user():
    if 'user_id' in session:
        user_id = session['user_id']
        try:
            auth2.delete_user(user_id)

            db.child('Users').child(user_id).remove()
            
            auth.current_user = None
            session.clear()

            flash('User successfully deleted.', 'success')
            return redirect(url_for('login_or_signup.login_or_signup_home'))
        except Exception as e:
            print(e)
            flash('Failed to delete user.', 'error')
            return redirect(url_for('dashboard.user_dashboard'))
    else:
        return redirect(url_for('login_or_signup.login_or_signup_home'))