#from flask import session
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

users_tags = db.Table('users_tags',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                       )

users_subtags = db.Table('users_subtags',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('subtag_id', db.Integer, db.ForeignKey('subtag.id'), primary_key=True)
                       )

users_interested_tags = db.Table('users_interested_tags',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
                       )

users_interested_subtags = db.Table('users_interested_subtags',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('subtag_id', db.Integer, db.ForeignKey('subtag.id'), primary_key=True)
                       )

friends = db.Table('friends',
                   db.Column('user1_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                   db.Column('user2_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                   )

student_associations_users =db.Table('student_associations_users',
                                     db.Column('student_association_id', db.Integer, db.ForeignKey('student_association.id'), primary_key=True),
                                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
                                     )

student_associations_tags =db.Table('student_associations_tags',
                                     db.Column('student_association_id', db.Integer, db.ForeignKey('student_association.id'), primary_key=True),
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
    name = db.Column(db.String())
    username = db.Column(db.String(), unique=True)
    bio = db.Column(db.String(), default='')
    
    free_hours = db.relationship('Hour', secondary=users_hours, backref='users')
    tags = db.relationship('Tag', secondary=users_tags, backref='users')
    subtags = db.relationship('SubTag', secondary=users_subtags, backref='users')
    
    interested_tags = db.relationship('Tag', secondary=users_interested_tags, backref='interested_users')
    interested_subtags = db.relationship('SubTag', secondary=users_interested_subtags, backref='interested_users')
    friend_list = db.relationship('User', secondary=friends, primaryjoin=(friends.c.user1_id == id),
                                  secondaryjoin=(friends.c.user2_id == id), backref=db.backref('followers'))
    

    def is_admin(self):
        admin_role = Role.query.filter_by(name='admin').first_or_404()
        return admin_role in self.roles

    def friend(self, user):
        if not self.is_friend(user):
            self.friend_list.append(user)
            user.friend_list.append(self)
            #return self
        
    def unfriend(self, user):
        if self.is_friend(user):
            self.friend_list.remove(user)
            user.friend_list.remove(self)
            #return self
        
    def is_friend(self, user):
        return user in self.friend_list
    
    def get_potential_teachers(self):
        current_subtags = set(self.interested_subtags)
        users = User.query.all()
        users = list(map(lambda x: [x, len(set(x.subtags) & current_subtags)], users))
        users.sort(key=lambda x: x[1])
        return list(reversed(users))

    def get_potential_cooperators(self):
        current_subtags = set(self.subtags)
        users = User.query.all()
        users = list(map(lambda x: [x, len(set(x.subtags) & current_subtags)], users))
        users.sort(key=lambda x: x[1])
        return list(reversed(users))
    
    def get_potential_coolearners(self):
        current_subtags = set(self.interested_subtags)
        users = User.query.all()
        users = list(map(lambda x: [x, len(set(x.interested_subtags) & current_subtags)], users))
        users.sort(key=lambda x: x[1])
        return list(reversed(users))

    def get_potential_students(self):
        current_subtags = set(self.subtags)
        users = User.query.all()
        users = list(map(lambda x: [x, len(set(x.interested_subtags) & current_subtags)], users))
        users.sort(key=lambda x: x[1])
        return list(reversed(users))

    def get_potential_friends(self):
        users = self.get_potential_teachers() + self.get_potential_cooperators() + self.get_potential_coolearners() + self.get_potential_students()
        users.sort(key=lambda x: x[1])

    def get_potential_friends_(self):
        potential_friends = db.session.query(User).filter(User.tags.overlap(self.tags)).all() #tags-tags
        potential_friends.append(db.session.query(User).filter(User.subtags.overlap(self.subtags)).all()) #subtags-subtags
        potential_friends.append(db.session.query(User).filter(User.interested_tags.overlap(self.tags)).all()) #tags-interested_tags
        potential_friends.append(db.session.query(User).filter(User.tags.overlap(self.interested_tags)).all()) #interested_tags-tags
        potential_friends.append(db.session.query(User).filter(User.interested_subtags.overlap(self.subtags)).all()) #subtags-interested_subtags
        potential_friends.append(db.session.query(User).filter(User.subtags.overlap(self.interested_subtags)).all()) #interested_subtags-subtags
        potential_friends.append(db.session.query(User).filter(User.interested_tags.overlap(self.interested_tags)).all()) #interested_tags-interested_tags
        potential_friends.append(db.session.query(User).filter(User.interested_subtags.overlap(self.interested_subtags)).all()) #interested_subtags-interested_subtags
        return potential_friends
        

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
    color = db.Column(db.String(), default='primary')

    def getsubtags_with_user(self, user: User):
        return list(filter(lambda x: x in user.subtags, self.subtags))

    def get_interested_subtags_with_user(self, user: User):
        return list(filter(lambda x: x in user.interested_subtags, self.subtags))
    
class SubTag(db.Model):
    __tablename__ = 'subtag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    
class StudentAssociation(db.Model):
    __tablename__ = 'student_association'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    info = db.Column(db.String(), unique=True)
    subscribers = db.relationship('User', secondary=student_associations_users, backref='student_associations')
    tags = db.relationship('Tag', secondary=student_associations_tags, backref='student_associations')


'''

ToDo:

'''