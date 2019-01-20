from flask import Flask, redirect, url_for, render_template, request
from database import Database, add_image, create_board, get_boards

app = Flask(__name__)


@app.route("/")
def index():
    return redirect(url_for('boards'))


@app.route("/boards", methods=['GET', 'POST'])
def boards():
    error = board_name = ''
    boards = get_boards()
    if request.method == 'POST':
        board_name = request.form['board_name']
        if not board_name:
            error = 'Please enter a name for your board'
        elif board_name in boards:
            error = 'That board name is already in use; please try another'
        else:
            create_board(board_name)
    return render_template('boards.html', boards=boards, value=board_name, error=error)


@app.cli.command('create-db')
def create_database():
    database = Database()
    database.create()


@app.cli.command('destroy-db')
def destroy_database():
    database = Database()
    database.destroy()
