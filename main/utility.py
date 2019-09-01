import sqlite3
from flask import Blueprint, flash, redirect, url_for, session
from functools import wraps
from sqlite3 import Error
from wtforms import SubmitField, PasswordField,  StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed

utility = Blueprint('utility', __name__)


# Update account form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])

# Register form class


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    confirm = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])

# Verifica che l'utente abbia effettuato il login e permette di accedere alle aree riservate solo agli utenti loggati


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Unauthorized, please login", 'danger')
            return redirect(url_for('users.login'))
    return wrap
