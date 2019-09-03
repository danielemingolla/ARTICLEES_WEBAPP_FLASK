from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from article.routes import articlesblueprint
from users.routes import users
from main.routes import mainroutes
from main.utility import utility

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myflaskapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='static/profilepics/default.png')
    username = db.Column(db.String(20), nullable=False)
    register_date = db.Column(db.DateTime, default=db.func.current_timestamp())


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(20), nullable=False)
    create_date = db.Column(db.DateTime, default=db.func.current_timestamp())


app.register_blueprint(users)
app.register_blueprint(articlesblueprint)
app.register_blueprint(mainroutes)
app.register_blueprint(utility)


if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(debug=True)
