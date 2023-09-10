from flask import Blueprint, request, jsonify
from .models import User, Tag, SubTag
from . import db
from flask_login import login_user, login_required, logout_user, current_user


api = Blueprint('api', __name__)

@api.route('/tags', methods=['PUT'])
def add_tags():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    tag_id = request.json['id']
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    current_user.tags.append(tag)
    db.session.commit()
    return jsonify({'success': 'ok'})

@api.route('/tags/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    tag = Tag.query.filter_by(id=tag_id).first_or_404()
    if tag not in current_user.tags:
        return jsonify({'error': 'user does not have tag'})
    current_user.tags.remove(tag)
    db.session.commit()
    return jsonify({'success': 'ok'})    

@api.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([{'id': tag.id, 'name': tag.name} for tag in tags])


@api.route('/tags/<int:tag_id>/subtagss', methods=['GET'])
def get_subtags(tag_id):
    tags = Tag.query.get(tag_id).subtags
    return jsonify([{'id': tag.id, 'name': tag.name} for tag in tags])


@api.route('/subtags', methods=['PUT'])
def add_subtags():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    subtag_id = request.json['id']
    subtag = SubTag.query.filter_by(id=subtag_id).first_or_404()
    tag = Tag.query.filter_by(id=subtag.tag_id).first_or_404()
    if tag  not in current_user.tags:
        return jsonify({'error': 'tag not added'})
    current_user.subtags.append(subtag)
    db.session.commit()
    return jsonify({'success': 'ok'})
    
@api.route('/subtags/<int:subtag_id>', methods=['DELETE'])
def delete_subtag(subtag_id):
    subtag = SubTag.query.filter_by(id=subtag_id).first_or_404()
    if subtag not in current_user.tags:
        return jsonify({'error': 'user does not have subtag'})
    tag = Tag.query.filter_by(id=subtag.tag_id).first_or_404()
    if tag  not in current_user.tags:
        return jsonify({'error': 'tag not added'})
    current_user.tags.remove(subtag)
    db.session.commit()
    return jsonify({'success': 'ok'})


@api.route('/user/friend', methods=['POST'])
def add_friend():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    user_id = request.json['id']
    user = User.query.filter_by(id=user_id).first_or_404()
    current_user.friend(user)
    db.session.commit()
    return jsonify({'success':'ok'})

@api.route('/user/friend', methods=['DELETE'])
def delete_friend():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    user_id = request.json['id']
    user = User.query.filter_by(id=user_id).first_or_404()
    current_user.unfriend(user)
    db.session.commit()
    return jsonify({'success':'ok'})

@api.route('/user/bio', methods=['PUT'])
def update_bio():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    new_bio = request.json['bio']
    current_user.bio = new_bio
    db.session.commit()
    return jsonify({'success':'ok'})


    
    
    
