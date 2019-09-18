import os
import secrets
from PIL import Image
from functools import wraps
from threading import Thread
from flask_mail import Message
from flask_wtf import FlaskForm
from articlee.models import Users
from wtforms.validators import ValidationError
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, PasswordField,  StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask import Blueprint, flash, redirect, url_for, session, render_template


utility = Blueprint('utility', __name__)


# Update account form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != session['username']:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                flash("That username is taken. Please choose a different one.", "danger")
                raise ValidationError()

    def validate_email(self, email):
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
    if 'default.png' not in old_photo_path.split('/'):
        os.remove('articlee/'+old_photo_path)
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        'articlee/static/profilepics', picture_fn).replace('\\', '/')
    # riduco dimensioni immagine, risparmio memoria e velocizzo il caricamento della pagina
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    print(picture_path)
    i.save(picture_path, quality=100, optimize=True)
    return picture_path.replace('articlee/', '')

# Sending email


def asynchronous(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper


@asynchronous
def send_async_email(app, msg):
    with app.app_context():
        from articlee import mail
        mail.send(msg)


def send_email(subject, sender, recipients, html_body):
    from run import app
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.html = html_body
    send_async_email(app, msg)


# Only works when Debug Mode is, avoid to access to thanks page
@utility.app_errorhandler(500)
def internal_server_error(e):
    flash("Unauthorized access!", 'danger')
    return redirect(url_for('mainroutes.index'))

# Different error handler for different error 404/405
@utility.app_errorhandler(404)
def page_not_found(e):
    return render_template('page/404.html'), 404


@utility.app_errorhandler(405)
def unauthorized_access(e):
    return render_template('page/405.html'), 405
