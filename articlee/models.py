from articlee import db
import datetime


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='static/profilepics/default.png')
    username = db.Column(db.String(20), nullable=False)
    register_date = db.Column(db.DateTime(
        timezone=True), default=datetime.datetime.utcnow)
    


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime, default=db.func.current_timestamp())


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    image_file = db.Column(db.String(25), nullable=False)
