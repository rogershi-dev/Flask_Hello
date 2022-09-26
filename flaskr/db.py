import sqlite3

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
                    current_app.config['DATABASE'],
                    detect_types = sqlite3.PARSE_DECLTYPES
                )
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db():
    db = get_db()
    #Only relative path is needed in open_resource() function
    #It's useful,since you won't know the exact loction during deployment process
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# The close_db() and init_db_command() functions need to be registered with the application instance.
# Since we're using a factory function,that instance is not available from start,
# Instead,we write a new function to do the work

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
