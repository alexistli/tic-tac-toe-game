"""Flask app routes."""
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

from app import socketio
from app.main import bp


@bp.route("/")
def index():
    """Shows the website index."""
    return render_template("index_socket.html", headline="Tic Tac Toe Game")


@bp.route("/game")
def game():
    """Shows the current game."""
    if "board" not in session:
        session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
        session["turn"] = "X"

    return render_template(
        "game.html", game=session["board"], turn=session["turn"], session=session
    )


@bp.route("/play/<int:row>/<int:col>")
def play(row, col):
    """Gets the coordinates of the played cell."""
    session["board"][row][col] = session["turn"]
    return redirect(url_for("main.game"))


@socketio.on("my event")
def handle_my_custom_event(json):
    """Handles socketio custom event."""
    print("received json: " + str(json))
