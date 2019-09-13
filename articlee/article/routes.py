from articlee import db
from flask_wtf import FlaskForm
from articlee.models import Articles
from articlee.main.utility import is_logged_in
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask import render_template, flash, redirect, url_for, session, request, Blueprint

articlesblueprint = Blueprint('articlesblueprint', __name__)


# Article form class

class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[
                        DataRequired(), Length(min=5, max=30)])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=30)])

# Lista articoli
@articlesblueprint.route('/articles')
def articles():
    articles = Articles.query.all()
    if articles:
        return render_template('page/articles.html', articles=articles)
    else:
        msg = 'No articles found!'
        return render_template('page/articles.html', msg=msg)


# Single article
@articlesblueprint.route('/article/<string:id>/')
def article(id):
    # Get article
    article = Articles.query.filter(Articles.id == id).first()
    return render_template('page/article.html', article=article)


# Add article
@articlesblueprint.route('/add_article', methods=["GET", "POST"])
@is_logged_in  # per accedere alla dashboard verifico che l'utente sia loggato
def add_article():
    form = ArticleForm(request.form)
    if form.validate_on_submit():
        article = Articles(title=form.title.data,
                           body=form.body.data, author=session['username'])
        db.session.add(article)
        db.session.commit()
        flash('Article created!', 'success')
        return redirect(url_for('.article', id=article.id))
    return render_template('page/add_article.html', form=form)


# Edit article
@articlesblueprint.route('/edit_article/<string:id>', methods=["GET", "POST"])
@is_logged_in  # per accedere alla dashboard verifico che l'utente sia loggato
def edit_article(id):
    article = Articles.query.filter(Articles.id == id).first()
    form = ArticleForm(request.form)
    if form.validate_on_submit():
        article.title = form.title.data
        article.body = form.body.data
        db.session.add(article)
        db.session.commit()
        flash('Article Update!', 'success')
        return redirect(url_for('.article', id=article.id))
    elif request.method == 'GET':
        form.title.data = article.title
        form.body.data = article.body
    return render_template('page/edit_article.html', form=form)

# Delete article
@articlesblueprint.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    Articles.query.filter(Articles.id == id).delete()
    db.session.commit()
    flash('Article Deleted!', 'success')
    return redirect(url_for('users.account'))
