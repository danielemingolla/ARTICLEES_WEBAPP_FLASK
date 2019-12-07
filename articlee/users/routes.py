from articlee import db
from sqlalchemy import or_
from passlib.hash import sha256_crypt
from articlee.models import Users, Articles
from flask import render_template, flash, redirect, url_for, session, request, Blueprint, jsonify
from articlee.main.utility import RegisterForm, is_logged_in, UpdateAccountForm, save_picture, send_email


users = Blueprint('users', __name__)

# API UTENTE


@users.route('/api/allusers/')
def allusers():
    dict_users = []
    user_all = Users.query.all()
    if user_all:
        for user in user_all:
            dict_users.append({"username": user.username, "name": user.name,
                               "email": user.email, "description": user.description, "image_file": user.image_file})
        return jsonify(dict_users)
    else:
        return jsonify({'message': 'No User in the database!'})


@users.route('/api/login/<string:username>/<string:password>')
def apilogin(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and sha256_crypt.verify(password, user.password):
        session['logged_in'] = True
        session['username'] = user.username
        session['email'] = user.email
        session['description'] = user.description
        dict = {"message": "success"}
        return jsonify(dict)
    else:
        dict = {"message": "error"}
        return jsonify(dict)


@users.route('/api/register/<string:username>/<string:name>/<string:hashed_password>/<string:email>')
def apiregister(username, name, hashed_password, email):
    if Users.query.filter(or_(Users.username == username, Users.email == email)).first():
        dict = {"message": "error"}
        return jsonify(dict)
    else:
        user = Users(name=name.replace(" ", ""), username=username.replace(" ", ""),
                     email=email.replace(" ", ""), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        dict = {"message": "success"}
        return jsonify(dict)


@users.route('/api/userinfo/<string:username>')
def apiuserinfo(username):
    user = Users.query.filter_by(username=username).first()
    if user:
        dict = {"username": user.username, "name": user.name,
                "email": user.email, "description": user.description, "image_file": user.image_file}
        return jsonify(dict)
    else:
        return jsonify({"message": "User doesn't exist!"})


@users.route('/api/userarticles/<string:username>')
def apiuserarticles(username):
    dict_articles = []
    user = Users.query.filter_by(username=username).first()
    articles = Articles.query.filter_by(author=username).all()
    if user:
        for article in articles:
            dict_articles.append({"author": article.author, "body": article.body,
                                  "title": article.title, "create_date": article.create_date, "id": article.id})
        return jsonify(dict_articles)
    else:
        return jsonify({"message": "User doesn't exist!"})


@users.route('/api/update/<string:myusername>/<string:username>/<string:avatar>/<string:email>/<string:description>')
def apiupdate(myusername, username, avatar, email, description):
    if (myusername == session['username']):
        user = Users.query.filter_by(username=username).first()
        Uemail = Users.query.filter_by(email=email).first()
        print(session['email'], session['username'])
        if user and username != session['username']:
            dict = {"message": "usernameexist"}
            return jsonify(dict)
        elif Uemail and email != session['email']:
            dict = {"message": "emailexist"}
            return jsonify(dict)
        else:
            updateuser = Users.query.filter_by(username=myusername).first()
            if avatar:
                picture_file = save_picture(avatar, updateuser.image_file)
                updateuser.image_file = picture_file
            session['username'] = updateuser.username = username
            session['email'] = updateuser.email = email
            updateuser.description = description
            db.session.add(updateuser)
            db.session.commit()
            dict = {"message": "update"}
            return jsonify(dict)
    else:
        dict = {"message": "nonauthorized"}
        return jsonify(dict)

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
        risposta = apilogin(username_candidate, password_candidate).get_json()
        if risposta['message'] == 'success':
            flash('You are now logged in', 'success')
            return redirect(url_for('users.account'))
        elif risposta['message'] == 'error':
            error = 'Invalid login'
            return render_template('page/login.html', error=error)
    return render_template('page/login.html')


# User Profile
@users.route('/account', methods=['GET', 'POST'])
@is_logged_in  # per accedere alla dashboard verifico che l'utente sia loggato
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        risposta = apiupdate(session['username'], form.username.data.replace(" ", ""), form.picture.data,
                             form.email.data.replace(" ", ""), form.description.data).get_json()
        if risposta['message'] == 'usernameexist':
            flash("Username already exists!", "danger")
        elif risposta['message'] == 'emailexist!':
            flash("Email already exists!", "danger")
        elif risposta['message'] == 'update':
            flash("Update correctly!", "success")
        else:
            flash("Permission denied!", "danger")
    elif request.method == 'GET':
        # campi compilati con i dati attuali prima dell'eventuale modifica
        infoutente = apiuserinfo(session['username']).get_json()
        form.username.data = infoutente['username']
        form.email.data = infoutente['email']
        form.description.data = infoutente['description']
    infoutente = apiuserinfo(session['username']).get_json()
    articoliutente = apiuserarticles(session['username']).get_json()
    return render_template('page/account.html', form=form, user=infoutente, articles=articoliutente)


# User register
@users.route('/register', methods=['GET', 'POST'])
def register():
    if 'logged_in' in session:
        flash("You are already login", 'danger')
        return redirect(url_for('users.account'))
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        risposta = apiregister(form.username.data, form.name.data, sha256_crypt.hash(
            str(form.password.data)), form.email.data).get_json()
        if risposta['message'] == 'error':
            flash("Change your email or username", 'danger')
        else:
            flash("Congratulations, you're registered!", 'success')
    return render_template('page/register.html', form=form)


# Logout
@users.route('/logout')
@is_logged_in  # per il logout devo prima essere loggato
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('users.login'))
