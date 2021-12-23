"""Flask app routes."""
from typing import Any
from typing import Dict
from typing import Union

from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug import Response

from app import socketio
from app.main import bp
from tic_tac_toe_game import engine
from tic_tac_toe_game.AI.mcts import mcts_best_move
from tic_tac_toe_game.AI.negamax import negamax_best_move
from tic_tac_toe_game.AI.random import random_move
from tic_tac_toe_game.engine import Board


@bp.route("/")
def index() -> str:
    """Shows the website index."""
    return render_template("index_socket.html", headline="Tic Tac Toe Game")


@bp.route("/game", methods=["GET", "POST"])
def game() -> Union[str, Response]:
    """Shows the current game."""
    current_game = session["game"]
    board = current_game.board
    turn = current_game.players_match.current().get_mark()
    chosen_cell = None

    if "choice" in request.form:
        row_str, col_str = request.form["choice"].split()
        chosen_cell = int(row_str), int(col_str)
        board.set_cell(coord=chosen_cell, value=turn)
        current_game.players_match.switch()

        if not board.is_full() and not board.is_winning_move(chosen_cell, turn):
            turn = current_game.players_match.current().get_mark()
            chosen_cell = current_game.get_move()
            board.set_cell(coord=chosen_cell, value=turn)
            current_game.players_match.switch()

    if chosen_cell is None:
        pass
    elif board.is_winning_move(chosen_cell, turn):
        return redirect(url_for("main.win", mark=turn))
    elif board.is_full():
        return redirect(url_for("main.tie"))

    if "AI_random" in request.form:
        current_game.players_match.update_ai_algorithm(random_move)
    elif "AI_mcts" in request.form:
        current_game.players_match.update_ai_algorithm(mcts_best_move)
    elif "AI_negamax" in request.form:
        current_game.players_match.update_ai_algorithm(negamax_best_move)
    print(current_game.players_match.players)

    return render_template("game.html", board=board.grid, turn=turn, session=session)


@bp.route("/win/<string:mark>")
def win(mark: str) -> str:
    """Announces the winning player."""
    return render_template("win.html", mark=mark)


@bp.route("/tie")
def tie() -> str:
    """Announces players are tied."""
    return render_template("tie.html")


@bp.route("/new_game")
def new_game() -> Response:
    """Initializes a new game."""
    if "game" not in session:
        current_game = engine.Engine("X", "B")
        current_game.players_match.update_ai_algorithm(random_move)
        session["game"] = current_game
    else:
        current_game = session["game"]
        current_game.players_match.switch()

    current_game.board = Board()

    return redirect(url_for("main.game"))


@socketio.on("my event")  # type: ignore[misc]
def handle_my_custom_event(json: Dict[str, Any]) -> None:
    """Handles socketio custom event."""
    print("received json: " + str(json))
