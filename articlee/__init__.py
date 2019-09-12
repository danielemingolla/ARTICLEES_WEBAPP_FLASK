from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myflaskapp.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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
