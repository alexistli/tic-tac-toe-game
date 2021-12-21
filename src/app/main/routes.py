"""Flask app routes."""
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from app import socketio
from app.main import bp
from tic_tac_toe_game import engine
from tic_tac_toe_game.engine import Grid
from tic_tac_toe_game.mcts_ai import compute_best_move

# from tic_tac_toe_game.negamax_ai import compute_best_move


@bp.route("/")
def index():
    """Shows the website index."""
    return render_template("index_socket.html", headline="Tic Tac Toe Game")


@bp.route("/game", methods=["GET", "POST"])
def game():
    """Shows the current game."""
    current_game = session["game"]
    grid = current_game.grid
    turn = current_game.players_match.current().get_mark()
    chosen_cell = None

    if "choice" in request.form:
        row_str, col_str = request.form["choice"].split()
        chosen_cell = int(row_str), int(col_str)

        grid.set_cell(coord=chosen_cell, value=turn)  # type: ignore[arg-type]

        current_game.players_match.switch()

        if not grid.is_full() and not grid.is_winning_move(chosen_cell, turn):
            turn = current_game.players_match.current().get_mark()
            chosen_cell = compute_best_move(turn, grid)

            grid.set_cell(coord=chosen_cell, value=turn)  # type: ignore[arg-type]

            current_game.players_match.switch()

    if chosen_cell is None:
        pass
    elif grid.is_winning_move(chosen_cell, turn):  # type: ignore[arg-type]
        return redirect(url_for("main.win", mark=turn))
    elif grid.is_full():
        return redirect(url_for("main.tie"))

    return render_template("game.html", board=grid.grid, turn=turn, session=session)


@bp.route("/win/<string:mark>")
def win(mark):
    """Announces the winning player."""
    return render_template("win.html", mark=mark)


@bp.route("/tie")
def tie():
    """Announces players are tied."""
    return render_template("tie.html")


@bp.route("/new_game")
def new_game():
    """Initializes a new game."""
    current_game = engine.Engine("X", "B")
    current_game.grid = Grid()

    session["game"] = current_game

    return redirect(url_for("main.game"))


@socketio.on("my event")
def handle_my_custom_event(json):
    """Handles socketio custom event."""
    print("received json: " + str(json))
