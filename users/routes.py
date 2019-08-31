from flask import Flask, render_template, flash, redirect, url_for, session, request, Blueprint
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_wtf import FlaskForm
from main.utility import create_connection, RegisterForm, is_logged_in, UpdateAccountForm
from passlib.hash import sha256_crypt

import sqlite3


users = Blueprint('users', __name__)


# User Profile
@users.route('/account', methods=['GET', 'POST'])
@is_logged_in  # per accedere alla dashboard verifico che l'utente sia loggato
def account():
    form = UpdateAccountForm(request.form)
    if form.validate_on_submit():
        newusername = form.username.data
        newemail = form.email.data
        db, cursor = create_connection()
        db1, cursor2 = create_connection()
        cursor.execute(
            "UPDATE users SET username=?,email=? WHERE username=?", (newusername, newemail, session['username']))
        db.commit()
        cursor2.execute("UPDATE articles SET author=? WHERE author=?", 
                        (newusername, session['username'])) #al cambio di username anche l'autore degli articoli cambia
        db1.commit()
        cursor2.close()
        cursor.close()
        session['username'] = newusername
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = session['username']
        form.email.data = session['email']
    # Create cursor
    _, cursor = create_connection()
    _, cursor2 = create_connection()
    # Get articles
    query1 = cursor.execute(
        "SELECT * FROM articles WHERE author=?", (session['username'],))
    query2 = cursor2.execute(
        "SELECT username,email FROM users WHERE username=?", (session['username'],))
    articles = query1.fetchall()
    datiUtente = query2.fetchall()[0]
    if articles:
        return render_template('page/account.html', articles=articles, form=form, datiUtente=datiUtente)
    else:
        return render_template('page/account.html', form=form, datiUtente=datiUtente)


# User register
@users.route('/register', methods=['GET', 'POST'])
def register():
    if 'logged_in' in session:
        flash("You are already login", 'danger')
        return redirect(url_for('users.account'))
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.hash(str(form.password.data))
        db, cursor1 = create_connection()
        cursor1.execute("SELECT email FROM users WHERE email=?", (email,))
        _, cursor2 = create_connection()
        cursor2.execute(
            "SELECT username FROM users WHERE username=?", (username,))
        result1 = cursor1.fetchone()
        result2 = cursor2.fetchone()
        if result1 and result2:
            flash("The email and username still exists both!", 'danger')
        elif result1:
            flash("The email still exists!", 'danger')
        elif result2:
            flash("The username still exists!", 'danger')
        else:
            cursor1.execute("INSERT INTO users(name,email,username,password) VALUES (?,?,?,?)",
                            (name, email, username, password))
            db.commit()
            flash("You are now registered and can log in", 'success')
            redirect(url_for('users.account'))
        cursor1.close()
        cursor2.close()
    return render_template('page/register.html', form=form)


# User Login
@users.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash("You are already log-in", 'danger')
        return redirect(url_for('users.account'))
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']
        # Create cursor
        _, cursor = create_connection()
        result = cursor.execute(
            "SELECT COUNT(*) FROM users WHERE username = ?", [username]).fetchone()
        if result[0] > 0:  # verifico che ci sia un utente registrato con quell'username
            # Get stored hash
            data = cursor.execute(
                "SELECT * FROM users WHERE username = ?", [username]).fetchone()
            # password si trova al 5 posto nella tupla restituita da fetchone()
            # Close connection
            cursor.close()
            password = data[4]
            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                _, cursor = create_connection()
                qEmail = cursor.execute("SELECT email from users WHERE username=?", [
                                        username]).fetchone()
                cursor.close()
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['email'] = qEmail[0]
                flash('You are now logged in', 'success')
                return redirect(url_for('users.account'))
            else:
                error = 'Invalid login'
                return render_template('page/login.html', error=error)
            # Close connection
            cursor.close()
        else:
            error = 'Username not found'
            return render_template('page/login.html', error=error)
    return render_template('page/login.html')


# Logout
@users.route('/logout')
@is_logged_in  # per il logout devo prima essere loggato
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('users.login'))
