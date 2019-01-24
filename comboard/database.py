from flask import g
import sqlite3
from comboard import comboard_app


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(comboard_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def create_db():
    db = get_db()
    with comboard_app.open_resource('schema.sql') as f:
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
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('INSERT INTO boards (name) VALUES (?)', (name,))
        return cursor.lastrowid


def delete_board(board_id):
    execute('DELETE FROM boards WHERE id = ?', (board_id,))


def get_boards():
    return fetchall('SELECT id, name FROM BOARDS')


def get_board(board_id):
    return fetchone('SELECT id, name from BOARDS WHERE id = ?', (board_id,))


def add_image(filename, board_id):
    execute('INSERT INTO images (filename, board_id) VALUES (?, ?)',
            (filename, board_id,))


def delete_image(id):
    execute('DELETE FROM images WHERE id = ?', (id,))


def get_images(board_id):
    return fetchall('SELECT filename FROM images WHERE board_id = ?', (board_id,))
