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

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

class User(UserMixin, db.Model):
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
    id = db.Column(db.Integer, primary_key=True)

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