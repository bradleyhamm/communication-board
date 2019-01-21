import sqlite3


class Database(object):

    def __init__(self):
        self.connection = sqlite3.connect('data.db')
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def create(self):
        self.cursor.executescript('''
            DROP TABLE IF EXISTS boards;
            CREATE TABLE IF NOT EXISTS boards (
                id integer PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL UNIQUE
            );

            DROP TABLE IF EXISTS images;
            CREATE TABLE IF NOT EXISTS images (
                id integer PRIMARY KEY AUTOINCREMENT,
                filename text NOT NULL UNIQUE,
                board_id integer NOT NULL,
                FOREIGN KEY (board_id) REFERENCES boards(id)
            );
        ''')
        self.connection.commit()

    def destroy(self):
        self.cursor.execute('''
            DROP TABLE IF EXISTS images;
            DROP TABLE IF EXISTS boards;
        ''')
        self.connection.commit()


def create_board(name):
    db = Database()
    db.cursor.execute('INSERT INTO boards (name) VALUES (?)', (name,))
    db.connection.commit()


def get_boards():
    db = Database()
    db.cursor.execute('SELECT id, name FROM BOARDS')
    return db.cursor.fetchall()


def get_board(board_id):
    db = Database()
    db.cursor.execute('SELECT id, name from BOARDS WHERE id = ?', (board_id,))
    return db.cursor.fetchone()


def add_image(filename, board_id):
    db = Database()
    db.cursor.execute('INSERT INTO images (filename, board_id) VALUES (?, ?)',
                      (filename, board_id,))
    db.connection.commit()


def get_images(board_id):
    db = Database()
    db.cursor.execute('SELECT filename FROM images WHERE board_id = ?', (board_id,))
    return db.cursor.fetchall()
