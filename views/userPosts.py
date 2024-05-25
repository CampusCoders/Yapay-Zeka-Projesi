from flask import Flask, request, jsonify, render_template, Blueprint, url_for, redirect, session, flash
from views.loginorsignup import db, auth2, auth

user_posts = Blueprint('user_posts', import_name=__name__, template_folder='templates')

@user_posts.route('/myPosts')
def my_posts():
    user_id = session.get('user_id')
    user_posts = db.child('Events').order_by_child('user_id').equal_to(user_id).get().val()
    if user_posts:
        return render_template('userposts.html', user_posts=user_posts)
    else:
        return render_template('userposts.html', user_posts=None)
    
@user_posts.route('/deletePost/<post_id>', methods=['POST'])
def delete_post(post_id):
    db.child('Events').child(post_id).remove()
    print('Post successfully deleted!')
    return redirect(url_for('user_posts.my_posts'))

