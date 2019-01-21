from app import app
from database import create_db


@app.cli.command('create-db')
def create_database():
    create_db()
