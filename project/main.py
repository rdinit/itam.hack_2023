from flask import Blueprint, render_template
from . import db
from flask_login import login_required, current_user
from .models import User


main = Blueprint('main', __name__)
@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index_for_user.html', user=current_user)
    return render_template('index.html')

@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', current_user=current_user, user=user)

@main.route('/profile/<username>/add_to_friends', methods=['POST'])
@login_required
def add_friend(username):
    user2 = User.query.filter_by(username=username).first_or_404()
    current_user.friend(user2)
    db.session.commit()
    return 'ok'#user1.friend_list[0].username + user2.friend_list[0].username
