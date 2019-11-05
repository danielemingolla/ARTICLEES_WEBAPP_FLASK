from articlee import db
from sqlalchemy import or_
from passlib.hash import sha256_crypt
from articlee.models import Users, Articles
from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from articlee.main.utility import RegisterForm, is_logged_in, UpdateAccountForm, save_picture, send_email


users = Blueprint('users', __name__)


# User Profile
@users.route('/account', methods=['GET', 'POST'])
@is_logged_in  # per accedere alla dashboard verifico che l'utente sia loggato
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        user = Users.query.filter(
            Users.username == session['username']).first()
        if form.picture.data:
            picture_file = save_picture(form.picture.data, user.image_file)
            user.image_file = picture_file
        usernameCanditato = form.username.data.replace(" ", "")
        if Users.query.filter(
                Users.username == form.username.data.replace(" ", "")).first() and usernameCanditato != session['username']:
            flash('Your username already exists!', 'danger')
            return redirect(url_for('users.account'))
        else:
            session['username'] = form.username.data.replace(" ", "")
            user.username = form.username.data.replace(" ", "")
            user.email = form.email.data.replace(" ", "")
            user.description = form.description.data
            db.session.add(user)
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # campi compilati con i dati attuali prima dell'eventuale modific
        user = Users.query.filter(
            Users.username == session['username']).first()
        form.username.data = user.username
        form.email.data = user.email
        form.description.data = user.description
    user = Users.query.filter(
        Users.username == session['username']).first()
    articles = Articles.query.filter(
        Articles.author == session['username']).all()
    return render_template('page/account.html', form=form, user=user, articles=articles)


# User register
@users.route('/register', methods=['GET', 'POST'])
def register():
    if 'logged_in' in session:
        flash("You are already login", 'danger')
        return redirect(url_for('users.account'))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        if Users.query.filter(or_(Users.username == form.username.data, Users.email == form.email.data)).first():
            flash("Change your email or username", 'danger')
        else:
            hashed_password = sha256_crypt.hash(str(form.password.data))
            user = Users(name=form.name.data.replace(" ", ""), username=form.username.data.replace(" ", ""),
                         email=form.email.data.replace(" ", ""), password=hashed_password)
            db.session.add(user)
            db.session.commit()
            '''
            send_email('%s you\'re registered to Articlee!' % form.username.data.upper(
            ), "calisthenicsbeginner98ta@gmail.com", form.email.data.split(), render_template('page/email.html', user=user))#
            '''
            flash("Congratulations, you're registered!", 'success')
    return render_template('page/register.html', form=form)


# User Login
@users.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash("You are already log-in", 'danger')
        return redirect(url_for('users.account'))
    if request.method == 'POST':
        # Get Form Fields
        username_candidate = request.form['username'].replace(" ", "")
        password_candidate = request.form['password'].replace(" ", "")
        user = Users.query.filter_by(username=username_candidate).first()
        if user and sha256_crypt.verify(password_candidate, user.password):
            session['logged_in'] = True
            session['username'] = username_candidate
            session['email'] = user.email
            session['description'] = user.description
            flash('You are now logged in', 'success')
            return redirect(url_for('users.account'))
        else:
            error = 'Invalid login'
            return render_template('page/login.html', error=error)
    return render_template('page/login.html')


# Logout
@users.route('/logout')
@is_logged_in  # per il logout devo prima essere loggato
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('users.login'))
