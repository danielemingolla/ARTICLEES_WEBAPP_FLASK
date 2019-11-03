from articlee.models import Articles
from flask import Blueprint, render_template


mainroutes = Blueprint('mainroutes', __name__)
# Index
@mainroutes.route('/')
def index():
    latest_articles=Articles.query.order_by(Articles.id.desc()).all()[:6]
    return render_template("page/home.html", latest_articles=latest_articles)

# About
@mainroutes.route('/about')
def about():
    return render_template('page/about.html')

# Contact
@mainroutes.route('/contact')
def contact():
    return render_template('page/contact.html')
