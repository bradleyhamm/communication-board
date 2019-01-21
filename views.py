import sqlite3
from flask import redirect, url_for, request, render_template
from app import app
from database import create_board, get_boards, get_board, get_images


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


@app.route("/boards/<board_id>", methods=['GET', 'POST'])
def board(board_id):
    error = ''
    if request.method == 'POST':
        if 'image' not in request.files:
            error = 'No file given'
        file = request.files['image']
        if not file.filename:
            error = 'Please select a file'
        # if file and
    board = get_board(board_id)
    images = get_images(board_id)
    return render_template('board.html', board=board, images=images, error=error)
