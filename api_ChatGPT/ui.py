from flask import Flask, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import interface

app = Flask(__name__)

@app.route('/')
def home():
    post_content = interface.get_post(
        "Genç Girişimciler İnovasyon Zirvesi",
        "Teknoloji ve İnovasyonun Geleceği",
        "Genç girişimcileri desteklemek ve yeni teknolojiler hakkında bilgi vermek",
        "Girişimci ruha sahip üniversite öğrencileri, start-up kurucuları ve teknoloji meraklıları",
        "Zoom",
        "Elif Demir, Murat Yılmaz, Seher Aydın",
        "Cem Kara",
        "TeknoYatırım, StartUpHub, InnoTech",
        "#GençGirişimcilerZirvesi #TeknolojiVeİnovasyon #Startup2024",
        "30 Mayıs 2024, 14:00 - 17:30",
        "Genç Girişimciler İnovasyon Zirvesi, genç girişimcileri desteklemek ve onlara teknolojinin en yeni trendleri hakkında bilgi sağlamak amacıyla düzenlenmektedir. Etkinlik, deneyimli konuşmacılar tarafından sunulan ilham verici konuşmalar ve interaktif workshoplar içerecek.",
        "event_link.com"
    )
    return render_template('post.html', post_content=post_content)

if __name__ == '__main__':
    app.run(debug=True)