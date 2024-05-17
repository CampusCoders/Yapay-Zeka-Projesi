from flask import Flask, request, jsonify, render_template, Blueprint
from api_ChatGPT import interface

create_event = Blueprint('create_event',import_name=__name__, template_folder='templates')

@create_event.route('/createEvent', methods=['POST'])
def create_event_from_API():
    event_name = request.form['etkinlikAdi']
    event_topic = request.form['etkinlikKonusu']
    event_purpose = request.form['etkinlikAmaci']
    event_target_audience = request.form['etkinlikHedefKitle']
    event_platform = request.form['etkinlikPlatformu']    
    event_participants = request.form['etkinlikKatilimcilari']
    event_hosts = request.form['etkinlikModeratörü']  
    event_sponsors = request.form['etkinlikSponsorlari'] 
    event_tags = request.form['etkinlikSosyalMedyaTagleri']
    event_date_and_time = request.form['etkinlikTarihiVeSaati']
    event_details = request.form['etkinlikDetaylari']
    event_link = request.form['etkinlikKayitKatilim']

    post_content = interface.get_post(event_name, event_topic, event_purpose, event_target_audience, event_platform,
                      event_participants, event_hosts, event_sponsors, event_tags, event_date_and_time,
                      event_details, event_link)
    print(post_content)
    
    return render_template('post.html', post_content=post_content)


