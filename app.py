from flask import Flask, flash, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from article.routes import articlesblueprint
from users.routes import users
from main.routes import mainroutes
from main.utility import utility
from shop.routes import shopblueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myflaskapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.register_blueprint(users)
app.register_blueprint(articlesblueprint)
app.register_blueprint(mainroutes)
app.register_blueprint(utility)
app.register_blueprint(shopblueprint)

# Only works when Debug Mode is, avoid to access to thanks page
@app.errorhandler(500)
def internal_server_error(e):
    flash("Unauthorized access!", 'danger')
    return redirect(url_for('mainroutes.index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page/404.html'), 404


@app.errorhandler(405)
def unauthorized_access(e):
    return render_template('page/405.html'), 405


if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(debug=True)
