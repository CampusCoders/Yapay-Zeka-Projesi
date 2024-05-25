from flask import Flask, request, jsonify, render_template, Blueprint, url_for, redirect, session, flash
from api_ChatGPT import interface
from views.loginorsignup import db, auth2, auth
from datetime import datetime

create_event = Blueprint('create_event', import_name=__name__, template_folder='templates')

@create_event.route('/createEvent')
def createEvent():
    return redirect(url_for('login_or_signup.logged'))

@create_event.route('/createEventFromIndex', methods=['POST'])
def create_event_from_API():
        user_id = session.get('user_id')
        user_data = db.child('Users').child(user_id).get().val()

        if user_data['daily_rights'] == 0 and 'create_event_button' in request.form:
            flash("Yetersiz hak!", "error")
            return redirect(url_for('create_event.createEvent'))
        
        elif user_data['daily_rights'] == 0 and 'create_event_button2' in request.form:
            flash("Yetersiz hak!", "error")
            return redirect(url_for('create_event.event_created'))

        if 'event_name' not in session:  
            session['event_name'] = request.form['etkinlikAdi']
            session['event_topic'] = request.form['etkinlikKonusu']
            session['event_purpose'] = request.form['etkinlikAmaci']
            session['event_target_audience'] = request.form['etkinlikHedefKitle']
            session['event_platform'] = request.form['etkinlikPlatformu']
            session['event_participants'] = request.form['etkinlikKatilimcilari']
            session['event_hosts'] = request.form['etkinlikModeratörü']
            session['event_sponsors'] = request.form['etkinlikSponsorlari']
            session['event_tags'] = request.form['etkinlikSosyalMedyaTagleri']
            session['event_date_and_time'] = request.form['etkinlikTarihiVeSaati']
            session['event_details'] = request.form['etkinlikDetaylari']
            session['event_link'] = request.form['etkinlikKayitKatilim']

        event_name = session.get('event_name')
        event_topic = session.get('event_topic')
        event_purpose = session.get('event_purpose')
        event_target_audience = session.get('event_target_audience')
        event_platform = session.get('event_platform')
        event_participants = session.get('event_participants')
        event_hosts = session.get('event_hosts')
        event_sponsors = session.get('event_sponsors')
        event_tags = session.get('event_tags')
        event_date_and_time = session.get('event_date_and_time')
        event_details = session.get('event_details')
        event_link = session.get('event_link')

        post_content = interface.get_post(
            event_name, event_topic, event_purpose, event_target_audience, event_platform,
            event_participants, event_hosts, event_sponsors, event_tags, event_date_and_time,
            event_details, event_link
        )
        print(post_content)

        session['post_content'] = post_content

        daily_rights = user_data['daily_rights']
        db.child('Users').child(user_id).update({'daily_rights': daily_rights -1 })

        create_date = datetime.now().strftime("%b %d, %Y at %H:%M:%S UTC+3")
        post_data = {
            'content': post_content,
            'shared_with': "none",
            'created_at': create_date,
            'user_id': user_id
        }

        db.child('Events').push(post_data)

        return redirect(url_for('create_event.event_created'))


@create_event.route('/event_created')
def event_created():
    if 'user_id' in session:
        user_id = session['user_id']
        user_data = db.child('Users').child(user_id).get().val()
        post_content = session['post_content']
        return render_template('post.html', post_content=post_content, user=user_data)
    else:
        return redirect(url_for('login_or_signup.login_or_signup_home'))
    


