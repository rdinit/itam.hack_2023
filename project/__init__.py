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

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/test1'

    db.init_app(app)
    with app.app_context():
        db.create_all()

    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User, Hour, Role


    admin = Admin(app, name='admin', index_view=MyIndexView())
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Role, db.session))
    with app.app_context():
        if FILL_DB == "1" and len(Role.query.filter_by().all()) < 2:
            try:
                admin_role = Role(name='admin')
                db.session.add(admin_role)
                db.session.add(Role(name='user'))
                db.session.commit()
                ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin'
                db.session.add(User(email='email@example.com', name='admin', roles=[admin_role],
                                    password=generate_password_hash(ADMIN_PASSWORD, method='scrypt')))
                for i in range(14*24):
                    db.session.add(Hour())
                db.session.commit()#'''
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

    from .frontend import frontend as frontend_blueprint
    app.register_blueprint(frontend_blueprint)


    return app