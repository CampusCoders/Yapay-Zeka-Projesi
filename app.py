from flask import Flask, render_template
from views.firebase import firebase_app
from views.chatbot import chatbot_app
import secrets


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Firebase uygulaması için Blueprint'i kaydet
app.register_blueprint(firebase_app)

# Chatbot uygulaması için Blueprint'i kaydet
app.register_blueprint(chatbot_app)

@app.route('/')
def index():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(debug=True)
