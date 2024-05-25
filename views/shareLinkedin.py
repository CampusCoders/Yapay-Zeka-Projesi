from flask import request, redirect, render_template, Blueprint, session, url_for
from LinkedinAPI.token_utils import refresh_token, args, authorize, parse_redirect_uri
from views.loginorsignup import db, auth2, auth

linkedin = Blueprint('linkedin',import_name=__name__, template_folder='templates')

@linkedin.route('/linkedinAuth', methods=['POST'])
def auth():
    api_url = 'https://www.linkedin.com/oauth/v2'
    authorize(api_url, *args)
    return render_template('linkedin.html')
    
def get_url():
    auth_code = redirect_response = request.form['redirect_url']
    auth_code = parse_redirect_uri(redirect_response)
    return auth_code

@linkedin.route('/getAccessToken', methods=['POST'])
def getAccessToken():
    auth_code = get_url()
    access_token = refresh_token(auth_code, *args)
    user_id = session['user_id']
    db.child('Users').child(user_id).update({'linkedin_access_token': access_token})
    return redirect(url_for('dashboard.user_dashboard'))
