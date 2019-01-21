import os
import time
import sqlite3
from flask import redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from app import app
from database import create_board, get_boards, get_board, get_images, add_image
from PIL import Image


ALLOWED_EXTENSIONS = 'png jpeg jpg gif'.split()
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024


def is_allowed_filetype(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return redirect(url_for('boards'))


@app.route("/boards", methods=['GET', 'POST'])
def boards():
    error = board_name = ''
    if request.method == 'POST':
        board_name = request.form['board_name']
        if not board_name:
            error = 'Please enter a name for your board'
        else:
            try:
                create_board(board_name)
            except sqlite3.IntegrityError:
                error = 'That board name is already in use; please try another'
    boards = get_boards()
    return render_template('boards.html', boards=boards, value=board_name, error=error)


def resize_image(file_path):
    image = Image.open(file_path)
    image.thumbnail((400, 400))
    image.save(file_path, image.format)


@app.route("/boards/<board_id>", methods=['GET', 'POST'])
def board(board_id):
    error = ''
    if request.method == 'POST':
        if 'image' not in request.files:
            error = 'Please select a file'
        else:
            file = request.files['image']
            if not file.filename:
                error = 'Please select a file'
            elif not is_allowed_filetype(file.filename):
                error = 'Only files with the following extensions are accepted: %s' % ', '.join(ALLOWED_EXTENSIONS)
            else:
                filename = '%s-%s' % (int(time.time()), secure_filename(file.filename))
                add_image(filename, board_id)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                resize_image(file_path)
                return redirect(url_for('board', board_id=board_id))
    board = get_board(board_id)
    images = get_images(board_id)
    return render_template('board.html', board=board, images=images, error=error)
