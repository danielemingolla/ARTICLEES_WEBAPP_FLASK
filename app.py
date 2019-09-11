from flask import Flask, flash, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from article.routes import articlesblueprint
from users.routes import users
from main.routes import mainroutes
from main.utility import utility
from shop.routes import shopblueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myflaskapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.register_blueprint(users)
app.register_blueprint(articlesblueprint)
app.register_blueprint(mainroutes)
app.register_blueprint(utility)
app.register_blueprint(shopblueprint)


if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(debug=True)
