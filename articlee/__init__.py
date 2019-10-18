import os
from flask import Flask, request
from .config import Config
from flask_mail import Mail
from flask_babel import Babel
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
babel = Babel()


#Get local language of the current user


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en','it'])

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    babel.init_app(app)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
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
    return app, manager

