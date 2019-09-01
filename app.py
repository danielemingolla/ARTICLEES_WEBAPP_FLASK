from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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
    username = db.Column(db.String(20), nullable=False)
    register_date = db.Column(db.DateTime, default=datetime.now)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(20), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now)


app.register_blueprint(users)
app.register_blueprint(articlesblueprint)
app.register_blueprint(mainroutes)
app.register_blueprint(utility)


'''
Tabella con autoincrement e ora locale funzionante

# CREATE TABLE articles (id INTEGER PRIMARY KEY AUTOINCREMENT,title VARCHAR(255), author VARCHAR(100), body TEXT, create_date TIMESTAMP DEFAULT(datetime('now', 'localtime')));

#CREATE TABLE users (id integer primary key,name VARCHAR(100) not null,email VARCHAR(100) not null,username VARCHAR(100) not null,password VARCHAR(30) NOT null,register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,unique (username, email));
'''

if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(debug=True)
