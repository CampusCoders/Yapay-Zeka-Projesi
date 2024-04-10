from flask import Flask, render_template, request, Blueprint, session
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

chatbot_app = Blueprint('chatbot_app', __name__, template_folder='templates')

@chatbot_app.route('/chatbot')
def chatbot_home():
    session['chat_history'] = []  # Her yeni oturumda chat history temizlenir
    return render_template('chatbot.html')

@chatbot_app.route("/startchatbot", methods=["POST"])
def chatbot():
    user_input = request.form["message"]
    prompt = f"User: {user_input}\nChatbot: "
    chat_history = session.get('chat_history', [])  # Oturumdan chat history alınır

    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.5,
        max_tokens=60,
        top_p=1,
        frequency_penalty=0,
        stop=["\nUser: ", "\nChatbot: "]
    )

    bot_response = response.choices[0].text.strip()
    chat_history.append({"speaker": "User", "message": user_input})
    chat_history.append({"speaker": "Chatbot", "message": bot_response})
    session['chat_history'] = chat_history  # Güncellenmiş chat history oturuma kaydedilir

    return render_template(
        "chatbot.html",
        chat_history=chat_history,
    )
