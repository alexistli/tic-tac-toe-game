"""Flask app routes."""
import logging
import sys
from typing import Union

from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug import Response

from app.main import bp
from tic_tac_toe_game import engine
from tic_tac_toe_game.AI import mcts
from tic_tac_toe_game.AI import naive
from tic_tac_toe_game.AI import negamax


FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(FORMATTER)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger.addHandler(console_handler)


@bp.route("/")
def index() -> str:
    """Shows the website index."""
    return render_template("index.html", headline="Tic Tac Toe Game")


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
        current_game.players_match.update_ai_algorithm(naive.naive_move)
    elif "AI_mcts" in request.form:
        current_game.players_match.update_ai_algorithm(mcts.mcts_move)
    elif "AI_negamax" in request.form:
        current_game.players_match.update_ai_algorithm(negamax.negamax_move)
    print(current_game.players_match.players)

    return render_template(
        "game.html", board=board.display(), turn=turn, session=session
    )


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
        current_game = engine.build_game()
        session["game"] = current_game
    else:
        current_game = session["game"]
        current_game.board = engine.Board()
        current_game.players_match.switch()

    return redirect(url_for("main.game"))


@bp.route("/move", methods=["POST"])
def move():
    """Processes a player's move."""
    player_move = request.form.get("move")

    print("/move")
    print(request.form)

    current_game = session["game"]
    board = current_game.board
    turn = current_game.players_match.current().get_mark()

    row_str, col_str = player_move.split()
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
        current_game.players_match.update_ai_algorithm(naive.naive_move)
    elif "AI_mcts" in request.form:
        current_game.players_match.update_ai_algorithm(mcts.mcts_move)
    elif "AI_negamax" in request.form:
        current_game.players_match.update_ai_algorithm(negamax.negamax_move)
    print(current_game.players_match.players)

    return render_template(
        "board.html", board=board.display(), turn=turn, session=session
    )
