import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from .config import Config

db = SQLAlchemy()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(Config)
    mail.init_app(app)
    db.init_app(app)

    from articlee.article.routes import articlesblueprint
    from articlee.users.routes import users
    from articlee.main.routes import mainroutes
    from articlee.main.utility import utility
    from articlee.shop.routes import shopblueprint
    app.register_blueprint(users)
    app.register_blueprint(articlesblueprint)
    app.register_blueprint(mainroutes)
    app.register_blueprint(utility)
    app.register_blueprint(shopblueprint)
    return app
