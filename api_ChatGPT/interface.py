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

def get_post(event_name, event_topic, event_purpose, target_audience, event_platform,
             participants, hosts, sponsors, social_media_tags, date_time, event_details, event_link):

    prompt = prompts.generate_prompt_full(
        event_name=event_name,
        event_topic=event_topic,
        event_purpose=event_purpose,
        target_audience=target_audience,
        event_platform=event_platform,
        participants=participants,
        hosts=hosts,
        sponsors=sponsors,
        social_media_tags=social_media_tags,
        date_time=date_time,
        event_details=event_details,
        event_link=event_link
    )

    messages = [
            {"role": "system", "content": system_message}, 
            {"role": "user", "content": prompt}
    ]


    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1
    )

    return completion.choices[0].message.content




#app = Flask(__name__)

#@app.route('/')
#def home():
#    post_content = get_post()
#    return render_template('post.html', post_content=post_content)

#if __name__ == '__main__':
#    app.run(debug=True)





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