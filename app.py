from flask import Flask, render_template, session, redirect, url_for
from views.loginorsignup import login_or_signup
from views.chatbot import chatbot_app
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Firebase uygulaması için Blueprint'i kaydet
app.register_blueprint(login_or_signup)

# Chatbot uygulaması için Blueprint'i kaydet
app.register_blueprint(chatbot_app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('login_or_signup.logged'))
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
