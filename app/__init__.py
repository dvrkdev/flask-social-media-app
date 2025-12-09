# __init__.py
import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

load_dotenv()


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
        static_url_path="/",
    )
    app.secret_key = os.environ.get("SECRET_KEY", "dev-fallback-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///social_media.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from .routes import auth, main

    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    login_manager.login_message = "Ushbu sahifani ko'rish uchun tizimga kiring!"
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
