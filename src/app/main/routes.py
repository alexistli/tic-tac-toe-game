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
    if "game" not in session:
        current_game = engine.Engine("X", "B")

        session["game"] = current_game
        # session["turn"] = current_game.players_match.current().get_mark()

    current_game = session["game"]
    grid = current_game.grid
    turn = current_game.players_match.current().get_mark()

    mark, played_cell = grid.get_last_play()
    print("get_last_play:", mark, played_cell)
    if not mark:
        pass
    elif grid.is_winning_move(played_cell, mark):  # type: ignore[arg-type]
        del session["game"]
        return redirect(url_for("main.win", mark=mark))
    elif grid.is_full():
        del session["game"]
        return redirect(url_for("main.tie"))

    # session["turn"] = current_game.players_match.current().get_mark()
    if turn == "O":
        chosen_cell = grid.random_available_cell()
        row, col = chosen_cell
        return redirect(url_for("main.play", row=row, col=col))

        # grid.set_cell(coord=played_cell, value=turn)  # type: ignore[arg-type]
        # current_game.players_match.switch()
        # session["turn"] = current_game.players_match.current().get_mark()

        # current_game.players_match.switch()

    return render_template("game.html", board=grid.grid, turn=turn, session=session)


@bp.route("/play/<int:row>/<int:col>")
def play(row, col):
    """Gets the coordinates of the played cell."""
    # session["board"][row][col] = session["turn"]

    current_game = session["game"]
    grid = current_game.grid
    turn = current_game.players_match.current().get_mark()

    grid.set_cell(coord=(row, col), value=turn)  # type: ignore[arg-type]

    # current_game.players_match.switch()
    # session["turn"] = current_game.players_match.current().get_mark()
    current_game.players_match.switch()

    return redirect(url_for("main.game"))


@bp.route("/win/<string:mark>")
def win(mark):
    """Announces the winning player."""
    return render_template("win.html", mark=mark)


@bp.route("/tie")
def tie():
    """Announces players are tied."""
    return render_template("tie.html")


@socketio.on("my event")
def handle_my_custom_event(json):
    """Handles socketio custom event."""
    print("received json: " + str(json))
