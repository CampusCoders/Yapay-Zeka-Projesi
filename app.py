from flask import Flask, render_template, session, redirect, url_for
from views.loginorsignup import login_or_signup
from views.createEvent import create_event
from views.dashboard import dashboard
from views.userPosts import user_posts
from views.linkedinToken import linkedinToken
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

app.register_blueprint(login_or_signup)

app.register_blueprint(dashboard)

app.register_blueprint(create_event)

app.register_blueprint(user_posts)

app.register_blueprint(linkedinToken)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('login_or_signup.logged'))
    else:
        return render_template('welcome.html')
    
if __name__ == '__main__':
    app.run(debug=True)
