from articlee import db
import datetime


'''
WARNING: Copy and paste without TAB
in PROJECTS/BLOG_WEBAPP_FLASK>
    from articlee import db, create_app
    app,_ = create_app()
    db.app = app
    with app.app_context():
        db.create_all()
    exit()
'''


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(51), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(55), nullable=False, unique=True)
    image_file = db.Column(db.String(100), nullable=False,
                           default='static/profilepics/default.png')
    username = db.Column(db.String(25), nullable=False, unique=True)
    register_date = db.Column(db.DateTime, default=datetime.datetime.now)


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.now)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Float)
    image_file = db.Column(db.String(100), nullable=False)
