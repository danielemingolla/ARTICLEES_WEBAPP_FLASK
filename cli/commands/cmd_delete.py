import os
import click
from articlee import db
from articlee import create_app
from articlee.models import Users, Articles


# Create an app context for the database connection.
app, _ = create_app()
db.app = app
# article delete <articles/users> <--count= INTEGER>


@click.command()
@click.option('--articles/--users', default=True, help='Delete rows in Users o Articles? DEFAULT: Articles')
@click.option('--count', default=1, type=click.IntRange(min=1), help='Number of row to delete. DEFAULT: 1 / ALLROWS: 9999')
@click.argument('path', default='articlee')
def cli(articles, count, path):
    """
    Delete latest 'count' (ordered by date) rows from Users or Articles table.
    """
    click.echo('\n\nUsers Total Rows: {}\nArticles total rows: {}\n'.format(
        Users.query.count(), Articles.query.count()))
    click.echo('Working...')
    if articles:
        deletedListArticles = Articles.query.order_by(
            Articles.create_date.desc()).limit(count).all()
        if count != 9999:
            print('ARTICOLI ELIMINATI: \n {}'.format(deletedListArticles))
            for deleteArticle in deletedListArticles:
                db.session.delete(deleteArticle)
        else:
            # Reset AUTO_INCREMENT of ID Column to zero
            db.session.execute('TRUNCATE Articles')
            Articles.query.delete()
    else:
        deletedListUsers = Users.query.order_by(
            Users.register_date.desc()).limit(count).all()
        if count != 9999:
            count = len(deletedListUsers)
            print('UTENTI ELIMINATI: \n {}'.format(deletedListUsers))
            for deleteUser in deletedListUsers:
                if 'default.png' not in deleteUser.image_file.split('/'):
                    os.remove('articlee/'+deleteUser.image_file)
                db.session.delete(deleteUser)
        else:
            deletedListUsers = Users.query.all()
            for deleteUser in deletedListUsers:
                if 'default.png' not in deleteUser.image_file.split('/'):
                    try:
                        os.remove('articlee/'+deleteUser.image_file)
                    except:
                        pass
                    # Reset AUTO_INCREMENT of ID Column to zero
                db.session.delete(deleteUser)
    db.session.commit()
    click.echo("I've finish. Rows deleted: {}".format(
        count if count != 9999 else "ALL"))
