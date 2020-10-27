import json
import requests
import lxml.html
from articlee.models import Articles
from flask import Blueprint, render_template, jsonify


mainroutes = Blueprint('mainroutes', __name__)

# API


@mainroutes.route('/api/index')
def apiindex():
    dict_article = []
    latest_articles = Articles.query.order_by(Articles.id.desc()).all()[:6]
    for article in latest_articles:
        dict_article.append({"title": article.title, "body": article.body, "id": article.id})
    return jsonify(dict_article)

# Index
@mainroutes.route('/')
def index():
    latest_articles = apiindex().get_json()
    for article in latest_articles:
        article['body'] = lxml.html.fromstring(article['body']).text_content()
    return render_template("page/home.html", latest_articles=latest_articles)

# About
@mainroutes.route('/about')
def about():
    return render_template('page/about.html')

# Contact
@mainroutes.route('/contact')
def contact():
    return render_template('page/contact.html')

# FAQ
@mainroutes.route('/faq')
def faq():
    return render_template('page/faq.html')
