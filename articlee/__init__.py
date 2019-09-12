from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myflaskapp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config['TESTING'] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')
    app.config['MAIL_MAX_EMAILS'] = 100
    app.config['MAIL_ASCII_ATTACHMENTS'] = False
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
