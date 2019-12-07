import click
import random
import secrets
from faker import Faker
from articlee import db
from articlee import create_app
from articlee.models import Users, Articles
from passlib.hash import sha256_crypt

# Create an app context for the database connection.
app, _ = create_app()
db.app = app
fake = Faker()

# article add <p-articles/p-users> <--count= INTEGER>


@click.command()
@click.option('--p-articles/--p-users', default=True, help='Populate Users o Article?')
@click.option('--count', default=1, type=click.IntRange(min=1), help='Number of row to generate.')
@click.argument('path', default='articlee')
def cli(p_articles, count, path):
    """
    Generate fake data to populate database.
    """
    click.echo('Working...')
    if p_articles:
        random_title = []
        for _ in range(count):
            random_title.append(fake.company())
        random_title = list(set(random_title))
        while True:
            if len(random_title) == 0:
                break
            fake_title = random_title.pop()
            # Scelto di un username random tra quelli degli utenti registrati
            random_author = random.choice(Users.query.all()).username
            fake_body = fake.text(max_nb_chars=999, ext_word_list=None)
            article = Articles(
                title=fake_title, author=random_author, body=fake_body)
            with app.app_context():
                db.session.add(article)
                db.session.commit()
    else:
        random_name = []
        for _ in range(count):
            random_name.append(fake.name())
        random_name = list(set(random_name))
        while True:
            if len(random_name) == 0:
                break
            fake_name = random_name.pop()
            fake_password = sha256_crypt.hash(str("daniele"))
            fake_email = fake.email()
            fake_username = fake.first_name()+secrets.token_hex(3)
            user = Users(name=fake_name, password=fake_password,
                         email=fake_email, username=fake_username)
            with app.app_context():
                db.session.add(user)
                db.session.commit()
    click.echo("I've finished. Rows generated: %d" % count)
