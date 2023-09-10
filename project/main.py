from flask import Blueprint, render_template
from . import db
from flask_login import login_required, current_user
from .models import SubTag, Tag, User


main = Blueprint('main', __name__)
@main.route('/')
def index():
    if current_user.is_authenticated:
        #recommend_users = рекомендации генерим
        return render_template('index_for_user.html', recommend_users=[current_user])#.get_potential_friends())
    return render_template('index.html')

@main.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', current_user=current_user, user=user)


@main.route('/at', methods=['GET'])
@login_required
def add_tag():
    tags = []
    for i in ['программирование', 'физика']:
        tags.append(Tag(name=i))
        db.session.add(tags[-1])
    db.session.commit()
    subtags = []
    for tag in tags:
        for i in range(3):
           subtags.append(SubTag(name=str(i) + tag.name, tag_id=tag.id))
           db.session.add(subtags[-1])
    db.session.commit()
    tag =Tag.query.get(1)
    subtags = tag.subtags
    current_user.tags.append(tag)
    db.session.commit()
    for subtag in subtags[:3]:
        current_user.subtags.append(subtag)
    db.session.commit()
    return len(current_user.subtags)

@main.route('/profile/<username>/add_to_friends', methods=['POST'])
@login_required
def add_friend(username):
    if username != current_user.username:
        user2 = User.query.filter_by(username=username).first_or_404()
        current_user.friend(user2)
        db.session.commit()
        return 'ok'#user1.friend_list[0].username + user2.friend_list[0].username
    return 418
