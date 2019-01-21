import os
import unittest
import tempfile
import sys
sys.path.append('..')
from app import app
import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        with app.app_context():
            database.create_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test__create_board(self):
        with app.app_context():
            database.create_board('Foo Board')
            self.assertListEqual([
                board['name'] for board in database.fetchall('SELECT name FROM boards')
            ], ['Foo Board'])

    def test__delete_board(self):
        with app.app_context():
            database.execute('INSERT INTO boards (name) VALUES (?)', ('Foo Board',))
            database.delete_board(1)
            self.assertEqual(len(database.get_boards()), 0)

    def test__get_boards(self):
        with app.app_context():
            self.assertEqual(len(database.get_boards()), 0)
            database.execute('INSERT INTO boards (name) VALUES (?)', ('Foo Board',))
            self.assertListEqual(list(map(tuple, database.get_boards())), [(1, 'Foo Board')])

    def test__get_board(self):
        with app.app_context():
            database.execute('''
                INSERT INTO boards (name)
                VALUES ('Foo Board'), ('Bar Board'), ('Baz Board')
            ''')
            board = database.fetchone('SELECT * FROM boards WHERE name = \'Bar Board\'')
            self.assertEqual(tuple(database.get_board(board['id'])), (2, 'Bar Board'))
