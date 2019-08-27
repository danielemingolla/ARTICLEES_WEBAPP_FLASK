from flask import Flask
from article.routes import articlesblueprint
from users.routes import users
from main.routes import mainroutes
from main.utility import utility

app = Flask(__name__)
app.register_blueprint(users)
app.register_blueprint(articlesblueprint)
app.register_blueprint(mainroutes)
app.register_blueprint(utility)


if __name__ == '__main__':
    app.secret_key = "secret123"
    app.run(debug=True)
