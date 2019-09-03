from flask import Blueprint, flash, redirect, url_for, session
from functools import wraps
from wtforms import SubmitField, PasswordField,  StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import ValidationError
from PIL import Image
import secrets
import os

utility = Blueprint('utility', __name__)


# Update account form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        from app import Users
        if username.data != session['username']:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                flash("That username is taken. Please choose a different one.", "danger")
                raise ValidationError()

    def validate_email(self, email):
        from app import Users
        if email.data != Users.query.filter(Users.username == session['username']).first().email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                flash("That email is taken. Please choose a different one.", "danger")
                raise ValidationError()
# Register form class


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=2, max=20)])
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

# Restituisce path dell'immagine da utilizzare come avatar rinominata con un token


def save_picture(form_picture, old_photo_path):
    # elimino foto profilo precedente prima di caricare la nuova
    if 'default' not in old_photo_path.split():
        os.remove(old_photo_path)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join('static\profilepics', picture_fn)
    output_size = (200, 200)  # riduco dimensioni immagine, risparmio memoria e velocizzo il caricamento della pagina
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path, quality=100, optimize=True)
    return picture_path
