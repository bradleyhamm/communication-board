from app import app
from database import Database


@app.cli.command('create-db')
def create_database():
    database = Database()
    database.create()


@app.cli.command('destroy-db')
def destroy_database():
    database = Database()
    database.destroy()
