import os
import time
import sqlite3
from flask import redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from comboard import comboard_app
from comboard.database import create_board, get_boards, get_board, get_images, add_image
from comboard.image import ImageFinder, resize_image


ALLOWED_EXTENSIONS = 'png jpeg jpg gif'.split()


def is_allowed_filetype(filename):
    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


@comboard_app.route("/")
def index():
    return redirect(url_for('boards'))


@comboard_app.route("/boards", methods=['GET', 'POST'])
def boards():
    auto_populate = False
    error = board_name = ''
    if request.method == 'POST':
        board_name = request.form['board_name']
        if not board_name:
            error = 'Please enter a name for your board'
        else:
            try:
                board_id = create_board(board_name)
            except sqlite3.IntegrityError:
                error = 'That board name is already in use; please try another'
            else:
                auto_populate = request.form.get('auto_populate', False)
                if auto_populate:
                    for filename in ImageFinder(board_name):
                        add_image(filename, board_id)
                return redirect(url_for('boards'))
    return render_template('boards.html', boards=get_boards(), board_name=board_name, auto_populate=auto_populate,
                           error=error)


@comboard_app.route("/boards/<board_id>", methods=['GET', 'POST'])
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
                file_path = os.path.join(comboard_app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                resize_image(file_path)
                return redirect(url_for('board', board_id=board_id))
    images = get_images(board_id)
    return render_template('board.html', board=get_board(board_id), images=images, error=error)
