from flask import Flask, request, jsonify, render_template, Blueprint, url_for, redirect, session, flash
from views.loginorsignup import db, auth2, auth
from LinkedinAPI.linkedin_post_create import get_user_profile, share_post, format_linkedin_content

user_posts = Blueprint('user_posts', import_name=__name__, template_folder='templates')

@user_posts.route('/myPosts')
def my_posts():
    user_id = session.get('user_id')
    user_data = db.child('Users').child(user_id).get().val()
    user_posts = db.child('Events').order_by_child('user_id').equal_to(user_id).get().val()
    linkedin_token = user_data.get('linkedin_access_token')

    if user_posts:
        if linkedin_token is None:
            return render_template('userposts.html', user_posts=user_posts)
        else:
            return render_template('userposts.html', user_posts=user_posts, linkedin_token=linkedin_token)
    else:
        return render_template('userposts.html', user_posts=None)
    
@user_posts.route('/deletePost/<post_id>', methods=['POST'])
def delete_post(post_id):
    db.child('Events').child(post_id).remove()
    print('Post successfully deleted!')
    return redirect(url_for('user_posts.my_posts'))

@user_posts.route('/shareLinkedin/<post_id>', methods=['POST'])
def sharePost(post_id):
    user_id = session['user_id']
    user_data = db.child('Users').child(user_id).get().val()
    linkedin_token = user_data.get('linkedin_access_token')

    user_post = db.child('Events').child(post_id).get().val()
    event_content = user_post.get('content')
    formatted_event_content = format_linkedin_content(event_content)
  
    user_profile = get_user_profile(linkedin_token)
    user_sub = user_profile.get('sub', '')
    if user_profile:
        print("User Profile:", user_profile)
    
    # Örnek bir post paylaşımı
    text_content = formatted_event_content
    share_result = share_post(linkedin_token, text_content, user_sub)
    if share_result:
        print("Post Shared:", share_result) 
    return redirect(url_for('user_posts.my_posts'))

@user_posts.route('/getPostDetails/<post_id>', methods=['GET'])
def get_post_details(post_id):
    user_post = db.child('Events').child(post_id).get().val()
    return jsonify(user_post)
