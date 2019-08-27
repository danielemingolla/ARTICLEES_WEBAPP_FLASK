import sqlite3
from flask import Blueprint, flash, redirect, url_for, session
from functools import wraps
from sqlite3 import Error
from wtforms import Form, StringField, TextAreaField, PasswordField, validators


utility = Blueprint('utility', __name__)


'''
Tabella con autoincrement e ora locale funzionante

# CREATE TABLE articles (id INTEGER PRIMARY KEY AUTOINCREMENT,title VARCHAR(255), author VARCHAR(100), body TEXT, create_date TIMESTAMP DEFAULT(datetime('now', 'localtime')));
'''
# Function for connecting to database


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('./myflaskapp.db')
        cursor = conn.cursor()
    except Error as e:
        print(e)
    return conn, cursor


# Register form class


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(
    ), validators.EqualTo('confirm', message='Passwords do not match')])  # deve essere uguale al campo 'confirm'
    confirm = PasswordField('Confirm Password')

# Verifica che l'utente abbia effettuato il login e permette di accedere a delle aree riservate solo agli utenti loggati


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please login", 'danger')
            return redirect(url_for('users.login'))
    return wrap
