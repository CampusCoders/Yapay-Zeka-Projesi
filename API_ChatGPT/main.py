from flask import Flask, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import prompts

_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)

models_newer = ["gpt-3.5-turbo", "gpt-4-turbo-preview", "gpt-4"]        #endpoint -> https://api.openai.com/v1/chat/completions
models_old = ["gpt-3.5-turbo-instruct", "babbage-002", "davinci-002"]   #endpoint -> https://api.openai.com/v1/completions

model = models_newer[0]
temperature = 1
max_tokens = 512
topic = ""

system_message = prompts.system_messages[3]
prompts = prompts.generate_prompt_full(
    event_name="Online Kariyer Geliştirme Zirvesi",
    event_topic="Kariyer Planlama ve Becerilerin Geliştirilmesi",
    event_purpose="Bu etkinlik, katılımcıların kariyerlerini planlamalarına ve geliştirmelerine yardımcı olmayı amaçlamaktadır. Uzman konuşmacılarımız, kariyer yolculuğuna yeni başlayanlar ve deneyimli profesyoneller için bilgi ve kaynaklar sunacaklar.",
    target_audience="Üniversite öğrencileri ve yeni mezunlar. Ayrıca, kariyerlerini ilerletmek ve yeni fırsatlar arayan herkes davetlidir.",
    event_platform="Zoom",
    participants="- Prof. Dr. Ayşe Yılmaz: Kariyer Planlama ve Stratejileri\n- Mehmet Ali Demir: Yeni Mezunlar İçin İş Arama Teknikleri\n- Nilgün Güner: Kişisel Marka Oluşturma ve LinkedIn Stratejileri",
    hosts="Deniz Karakoç ve Ali Can",
    sponsors="Turkcell",
    social_media_tags="#KariyerZirvesi #KariyerGelişimi #OnlineEtkinlik",
    date_time="12 Mayıs 2024, 10:00 - 16:00 (GMT+3)",
    event_details="Online Kariyer Geliştirme Zirvesi, kariyerlerini ilerletmek isteyen herkes için bilgi dolu bir gün sunuyor. Uzman konuşmacılarımızla interaktif oturumlar ve atölye çalışmalarıyla katılımcıları destekliyoruz. Etkinlik boyunca, katılımcılar kariyer hedeflerine ulaşmak için gerekli adımları öğrenecekler ve network kurma fırsatı bulacaklar.",
    event_link="www.kariyerzirvesi.com/kayit"
)

messages = [
            {"role": "system", "content": system_message}, 
            {"role": "user", "content": prompts}
        ]
 


def get_post():
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1
    )

    return completion.choices[0].message.content


app = Flask(__name__)

@app.route('/')
def home():
    post_content = get_post()
    return render_template('post.html', post_content=post_content)

if __name__ == '__main__':
    app.run(debug=True)





# gpt-3.5-turbo max input token = 4097

# List of Chat GPT Documentation
    # Tüm API örnekleri -> https://platform.openai.com/docs/api-reference/introduction
    # Text Generation Models -> https://platform.openai.com/docs/guides/text-generation
    # Prompt Engineering -> https://platform.openai.com/docs/guides/prompt-engineering
    # Prompt Examples -> https://platform.openai.com/examples


# Chat completion object
#{
#  "id": "chatcmpl-123",
#  "object": "chat.completion",
#  "created": 1677652288,
#  "model": "gpt-3.5-turbo-0125",
#  "system_fingerprint": "fp_44709d6fcb",
#  "choices": [{
#    "index": 0,
#    "message": {
#      "role": "assistant",
#      "content": "\n\nHello there, how may I assist you today?",
#    },
#    "logprobs": null,
#    "finish_reason": "stop"
#  }],
#  "usage": {
#    "prompt_tokens": 9,
#    "completion_tokens": 12,
#    "total_tokens": 21
#  }
#}
     

# Etkinlik Adı: Genç Girişimciler İnovasyon Zirvesi
# Etkinlik Konusu: Teknoloji ve İnovasyonun Geleceği
# Etkinlik Amacı: Genç girişimcileri desteklemek ve yeni teknolojiler hakkında bilgi vermek
# Hedef Kitle: Girişimci ruha sahip üniversite öğrencileri, start-up kurucuları ve teknoloji meraklıları
# Etkinlik Platformu: Zoom
# Katılımcılar/Konuşmacılar: Elif Demir, Murat Yılmaz, Seher Aydın
# Sunucular: Cem Kara
# Sponsorlar: TeknoYatırım, StartUpHub, InnoTech
# Sosyal Medya Tagleri: #GençGirişimcilerZirvesi #TeknolojiVeİnovasyon #Startup2024
# Tarih Saat: 30 Mayıs 2024, 14:00 - 17:30
# Etkinlik Hakkında Detaylar: Genç Girişimciler İnovasyon Zirvesi, genç girişimcileri desteklemek ve onlara teknolojinin en yeni trendleri hakkında bilgi sağlamak amacıyla düzenlenmektedir. Etkinlik, deneyimli konuşmacılar tarafından sunulan ilham verici konuşmalar ve interaktif workshoplar içerecek.