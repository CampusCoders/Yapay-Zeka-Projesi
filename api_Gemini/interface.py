from api_Gemini import prompts
import google.generativeai as genai
import markdown2

genai.configure(api_key="AIzaSyAhGHuv2iHGDnNiXmnZpt5Al6Ao9X07_PY")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel('gemini-1.5-flash')


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

    response = model.generate_content(prompt)

    text = markdown2.markdown(response.text)
     
    return text

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
