import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
import sqlalchemy
from werkzeug.security import generate_password_hash
from .admin_views import MyIndexView, MyModelView

    
db = SQLAlchemy()

FILL_DB = os.environ.get('FILL_DB')  # 1 or 0
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Hour, Role, Tag, SubTag, TagType
    



    admin = Admin(app, name='admin', index_view=MyIndexView())
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Role, db.session))
    with app.app_context():
        if FILL_DB == "1":
            pass    
            #add tags and subtags
            '''
            f = open('tags.txt', 'r').readlines()
            i = 2
            tag_name = f[0].rstrip()
            tag_color = f[1].rstrip()
            tag = Tag(name=tag_name, color=tag_color)
            db.session.add(tag)
            db.session.commit()
                

            tag_id = tag.id
            subtags = []
            while i < len(f):
                t = f[i].rstrip()
                if t != '$tag_split$':
                    subtags.append(SubTag(name=t, tag_id=tag_id))
                    db.session.add(subtags[-1])
                    db.session.commit()
                else:
                    tag.subtags = subtags
                    db.session.commit()
                    i += 1
                    if i < len(f):
                        tag_name = f[i].rstrip()
                        i += 1
                        tag_color = f[i].rstrip()
                        tag = Tag(name=tag_name, color=tag_color)
                        db.session.add(tag)
                        db.session.commit()
                        tag_id = tag.id
                        subtags = []
                i += 1
            db.session.commit()
            '''
        if FILL_DB == "1" and len(Role.query.filter_by().all()) < 2:
            try:
                admin_role = Role(name='admin')
                db.session.add(admin_role)
                db.session.add(Role(name='user'))
                db.session.commit()
                ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin'
                db.session.add(User(email='email@example.com', username='admin', roles=[admin_role],
                                    password=generate_password_hash(ADMIN_PASSWORD, method='scrypt')))
                for i in range(14*24):
                    db.session.add(Hour())
                db.session.commit()
                

            except sqlalchemy.exc.ProgrammingError:
                pass


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app