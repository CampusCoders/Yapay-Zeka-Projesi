from flask import request, redirect, render_template, Blueprint, session, url_for
from LinkedinAPI.linkedin_token_utils import refresh_token, args, authorize, parse_redirect_uri
from views.loginorsignup import db, auth2, auth
from datetime import datetime, timedelta

payment = Blueprint('payment',import_name=__name__, template_folder='templates')

@payment.route('/payment')
def subPayment():
    return render_template('payment.html')

@payment.route('/paymentSuccess')
def paymentSuccess():
    user_id = session['user_id']
    user_data = db.child('Users').child(user_id).get().val()
    sub_types = ['Free', 'Advanced']

    sub_types_descriptions = ['Free paket sadece etkinlik yazısı oluşturur.',
                                  'Advanced paket etkinlik yazısı, görsel oluşturma ve Linkedin API entegrasyonu içerir.']
        
    sub_daily_rights = ['5','30']

    # Mevcut tarihi al
    current_date = datetime.now()

    # 30 gün ekleyerek bitiş tarihini hesapla
    end_date = current_date + timedelta(days=30)

    # Bitiş tarihini belirli bir formata dönüştür
    end_date_formatted = end_date.strftime("%b %d, %Y at %H:%M:%S UTC+3")   
    
    user_data = {
            'sub_type': sub_types[1],
            'daily_rights': sub_daily_rights[1],
            'expire_date': end_date_formatted
        }

    sub_data = {
            'description': sub_types_descriptions[1],
            'price': 200,
            'price_currency': 'TL',
            'sub_daily_rights': sub_daily_rights[1],
            'sub_name': sub_types[1]
        }
    
    db.child('Users').child(user_id).update(user_data)

    db.child('Subscriptions').child(sub_types[1]).set(sub_data)
    
    return redirect(url_for('login_or_signup.login_or_signup_home'))
    
