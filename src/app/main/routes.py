"""Flask app routes."""
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for

from app import socketio
from app.main import bp
from tic_tac_toe_game import engine


@bp.route("/")
def index():
    """Shows the website index."""
    return render_template("index_socket.html", headline="Tic Tac Toe Game")


@bp.route("/game")
def game():
    """Shows the current game."""
    if "board" not in session:
        current_game = engine.Engine("X", "B")

        board = current_game.grid.grid

        session["board"] = board
        session["game"] = current_game
        session["turn"] = current_game.players_match.current().get_mark()

    current_game = session["game"]
    session["turn"] = current_game.players_match.current().get_mark()
    if session["turn"] == "O":
        played_cell = current_game.grid.random_available_cell()
        current_game.grid.set_cell(
            coord=played_cell, value=session["turn"]  # type: ignore[arg-type]
        )
        current_game.players_match.switch()
        session["turn"] = current_game.players_match.current().get_mark()

    return render_template(
        "game.html", game=session["board"], turn=session["turn"], session=session
    )


@bp.route("/play/<int:row>/<int:col>")
def play(row, col):
    """Gets the coordinates of the played cell."""
    session["board"][row][col] = session["turn"]

    current_game = session["game"]
    current_game.players_match.switch()
    session["turn"] = current_game.players_match.current().get_mark()

    return redirect(url_for("main.game"))


@socketio.on("my event")
def handle_my_custom_event(json):
    """Handles socketio custom event."""
    print("received json: " + str(json))
