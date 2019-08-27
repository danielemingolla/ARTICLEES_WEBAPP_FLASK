import sqlite3
from flask import Blueprint, render_template
from main.utility import is_logged_in
mainroutes = Blueprint('mainroutes', __name__)
# Index
@mainroutes.route('/')
def index():
    return render_template("page/home.html")

# About
@mainroutes.route('/about')
def about():
    return render_template('page/about.html')

# Dashboard
@mainroutes.route('/dashboard')
@is_logged_in  # per accedere alla dashboard verifico che l'utente sia loggato
def dashboard():
    # Create cursor
    db = sqlite3.connect('./myflaskapp.db')
    cursor = db.cursor()
    # Get articles
    result = cursor.execute("SELECT * FROM articles")
    articles = result.fetchall()
    if articles:
        return render_template('page/dashboard.html', articles=articles)
    else:
        msg = 'No articles found!'
        return render_template('page/dashboard.html', msg=msg)
    # Close connection
    cursor.close()
