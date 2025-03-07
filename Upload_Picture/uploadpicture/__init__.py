from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from datetime import timedelta
db = SQLAlchemy()

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")

def create_database(app):
    if not os.path.exists("uploadpicture/" + DB_NAME):
         with app.app_context():  # Sử dụng context của ứng dụng
            db.create_all()
            print("Created database")

print(SECRET_KEY)
print(DB_NAME)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    from .models import Img, User
    create_database(app)

    from .user import user
    from .views import views
    app.register_blueprint(user)
    app.register_blueprint(views)

    login_manager = LoginManager()
    login_manager.login_view = "user.login"
    login_manager.init_app(app)

    app.permanent_session_lifetime = timedelta(seconds=15)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app