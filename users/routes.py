from flask import Flask, render_template, flash, redirect, url_for, session, request,Blueprint
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from main.utility import create_connection, RegisterForm, is_logged_in
from passlib.hash import sha256_crypt
import sqlite3


users = Blueprint('users', __name__)


# User register
@users.route('/register', methods=['GET', 'POST'])
def register():
    if 'logged_in' in session:
        flash("You are already login", 'danger')
        return redirect(url_for('mainroutes.dashboard'))
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
            redirect(url_for('mainroutes.index'))
        cursor1.close()
        cursor2.close()
    return render_template('page/register.html', form=form)


# User Login
@users.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        flash("You are already log-in", 'danger')
        return redirect(url_for('mainroutes.dashboard'))
    if request.method == 'POST':
        db = sqlite3.connect('./myflaskapp.db')
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cursor = db.cursor()
        result = cursor.execute(
            "SELECT COUNT(*) FROM users WHERE username = ?", [username]).fetchone()
        if result[0] > 0:  # verifico che ci sia un utente registrato con quell'username
            # Get stored hash
            data = cursor.execute(
                "SELECT * FROM users WHERE username = ?", [username]).fetchone()
            # password si trova al 5 posto nella tupla restituita da fetchone()
            password = data[4]
            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('mainroutes.dashboard'))
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
