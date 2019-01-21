from flask import g
import sqlite3
from app import app

DATABASE_FILE = 'data.db'
app.config['DATABASE'] = DATABASE_FILE


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def create_db():
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))


def fetchone(query, params=()):
    with get_db() as db:
        return db.execute(query, params).fetchone()


def fetchall(query, params=()):
    with get_db() as db:
        return db.execute(query, params).fetchall()


def execute(query, params=()):
    with get_db() as db:
        db.execute(query, params)


def create_board(name):
    execute('INSERT INTO boards (name) VALUES (?)', (name,))


def delete_board(id):
    execute('DELETE FROM boards WHERE id = ?', (id,))


def get_boards():
    return fetchall('SELECT id, name FROM BOARDS')


def get_board(id):
    return fetchone('SELECT id, name from BOARDS WHERE id = ?', (id,))


def add_image(filename, board_id):
    execute('INSERT INTO images (filename, board_id) VALUES (?, ?)',
            (filename, board_id,))


def delete_image(id):
    execute('DELETE FROM images WHERE id = ?', (id,))


def get_images(board_id):
    return fetchall('SELECT filename FROM images WHERE board_id = ?', (board_id,))
