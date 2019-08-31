from main.utility import create_connection, is_logged_in
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, g,Blueprint
import sqlite3
articlesblueprint = Blueprint('articlesblueprint', __name__)

# Lista articoli
@articlesblueprint.route('/articles')
def articles():
    # Create cursor
    _, cursor = create_connection()
    # Get articles
    result = cursor.execute("SELECT * FROM articles")
    articles = result.fetchall()
    # Close connection
    cursor.close()
    if articles:
        return render_template('page/articles.html', articles=articles)
    else:
        msg = 'No articles found!'
        return render_template('page/articles.html', msg=msg)


# Single article
@articlesblueprint.route('/article/<string:id>/')
def article(id):
    _, cursor = create_connection()
    # Get article
    result = cursor.execute("SELECT * FROM articles WHERE id = ?", [id])
    article = result.fetchone()
    return render_template('page/article.html', article=article)


# Article form class

class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])

# Add article
@articlesblueprint.route('/add_article', methods=["GET", "POST"])
@is_logged_in  # per accedere alla dashboard verifico che l'utente sia loggato
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        # Create cursor
        db = sqlite3.connect('./myflaskapp.db')
        cursor = db.cursor()
        # Execute
        cursor.execute("INSERT INTO articles (title,body,author) VALUES (?,?,?)",
                       (title, body, session['username']))
        # Commit to DB
        db.commit()
        # Close connection
        cursor.close()
        flash('Article created!', 'success')
        return redirect(url_for('users.account'))
    return render_template('page/add_article.html', form=form)


# Edit article
@articlesblueprint.route('/edit_article/<string:id>', methods=["GET", "POST"])
@is_logged_in  # per accedere alla dashboard verifico che l'utente sia loggato
def edit_article(id):
    # Create cursor
    db = sqlite3.connect('./myflaskapp.db')
    cursor = db.cursor()

    # Get article by id
    result = cursor.execute("SELECT * FROM articles WHERE id = ?", [id])
    article = result.fetchone()
    # Get form
    form = ArticleForm(request.form)
    # Populate article form fields
    form.title.data = article[1]
    form.body.data = article[3]
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        # Create cursor
        db = sqlite3.connect('./myflaskapp.db')
        cursor = db.cursor()
        # Execute
        cursor.execute(
            "UPDATE articles SET title=?,body=? WHERE id=?", (title, body, id))
        # Commit to DB
        db.commit()
        # Close connection
        cursor.close()
        flash('Article Update!', 'success')
        return redirect(url_for('users.account'))
    return render_template('page/edit_article.html', form=form)

# Delete article
@articlesblueprint.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
     # Create cursor
    db = sqlite3.connect('./myflaskapp.db')
    cursor = db.cursor()

    # Execute
    cursor.execute("DELETE FROM articles where id=?", [id])
    db.commit()
    # Close connection
    cursor.close()
    flash('Article Deleted!', 'success')
    return redirect(url_for('users.account'))
