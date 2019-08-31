from flask import Blueprint, render_template
mainroutes = Blueprint('mainroutes', __name__)
# Index
@mainroutes.route('/')
def index():
    return render_template("page/home.html")

# About
@mainroutes.route('/about')
def about():
    return render_template('page/about.html')


