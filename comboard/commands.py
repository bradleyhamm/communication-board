from comboard import comboard_app
from comboard.database import create_db


@comboard_app.cli.command('create-db')
def create_database():
    create_db()
