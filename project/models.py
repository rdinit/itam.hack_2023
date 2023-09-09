from . import db
from flask_login import UserMixin


users_hours = db.Table('users_hours',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('hour_id', db.Integer, db.ForeignKey('hour.id'), primary_key=True)
                       )

users_roles = db.Table('users_roles',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
                       )

subtags = db.Table('subtags',
                   db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                   db.Column('subtag_id', db.Integer, db.ForeignKey('subtag.id'), primary_key=True)
                   )

tags = db.Table('tags',
                db.Column('tagtype_id', db.Integer, db.ForeignKey('tagtype.id'), primary_key=True),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                )

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    roles = db.relationship('Role', secondary=users_roles, backref='users')
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    name = db.Column(db.String(), unique=True)
    bio = db.Column(db.String())
    
    free_hours = db.relationship('Hour', secondary=users_hours, backref='users')
    #tags = #many to many
    #subtags = #many to many

class Hour(db.Model):
    __tablename__ = 'hour'
    id = db.Column(db.Integer, primary_key=True)


class TagType(db.Model):
    __tablename__ = 'tagtype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    tags = db.relationship('Tag')
    
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    tag_type_id = db.Column(db.Integer, db.ForeignKey('tagtype.id'))
    approved = db.Column(db.Boolean(), default=True)
    subtags = db.relationship('SubTag')
    
class SubTag(db.Model):
    __tablename__ = 'subtag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('type.id'))



'''

ToDo:
    # tagtype это сборка тэгов по темам, например, учеба, хобби, студобъединение
    # каждый тэг присвоен к типу тэгов. Например C++ к учебе
    # субтэг это подтема. Например у C++ может быть "синтаксис", "ООП", "Типы данных". Более узкие темы
    # 
    TagType:
        - name unique=True
        - tags [Tag]
        - 
    Tag:
        - name,
        - tag_type_id
        - subtags [Subtag]
        approved = db.Column(db.Boolean(), default=True)

    SubTag:
        - name
        - tag_id 
'''