from flask import render_template, flash, redirect, url_for, session, request, Blueprint
from main.utility import RegisterForm, is_logged_in, UpdateAccountForm, save_picture
from passlib.hash import sha256_crypt
from sqlalchemy import or_

users = Blueprint('users', __name__)


# User Profile
@users.route('/account', methods=['GET', 'POST'])
@is_logged_in  # per accedere alla dashboard verifico che l'utente sia loggato
def account():
    form = UpdateAccountForm()
    from models import Users, Articles
    if form.validate_on_submit():
        from app import db
        user = Users.query.filter(
            Users.username == session['username']).first()
        articles = Articles.query.filter(
            Articles.author == session['username']).all()
        if form.picture.data:
            picture_file = save_picture(form.picture.data, user.image_file)
            user.image_file = picture_file
        for article in articles:
            article.author = form.username.data
        user.username = form.username.data
        user.email = form.email.data
        session['username'] = form.username.data
        db.session.add(user, articles)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # campi compilati con i dati attuali prima dell'eventuale modifica
        form.username.data = session['username']
        form.email.data = Users.query.filter(
            Users.username == session['username']).first().email
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
        from app import db
        from models import Users
        if Users.query.filter(or_(Users.username == form.username.data, Users.email)).first():
            flash("Change your email or username", 'danger')
        else:
            hashed_password = sha256_crypt.hash(str(form.password.data))
            user = Users(name=form.name.data, username=form.username.data,
                         email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Congratulations, you're registered!", 'success')
    return render_template('page/register.html', form=form)


# User Login
@users.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash("You are already log-in", 'danger')
        return redirect(url_for('users.account'))
    if request.method == 'POST':
        from models import Users
        # Get Form Fields
        username_candidate = request.form['username']
        password_candidate = request.form['password']
        user = Users.query.filter_by(username=username_candidate).first()
        if user and sha256_crypt.verify(password_candidate, user.password):
            session['logged_in'] = True
            session['username'] = username_candidate
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
