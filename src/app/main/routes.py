"""Flask app routes."""
import logging
import sys
from typing import Union

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_socketio import join_room
from flask_socketio import leave_room
from flask_socketio import send
from werkzeug import Response

from app import socketio
from app.main import bp
from app.main.forms import CreateMultiGame
from app.main.forms import JoinMultiGame
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


@bp.route("/session", methods=["GET"])
def session_view():
    """Display session variable value."""
    return render_template(
        "session.html",
        title="Flask-Session Tutorial.",
        template="dashboard-template",
        session_variable=str(session),
        sid=request.s,
    )


@bp.route("/")
def index() -> str:
    """Shows the website index."""
    return render_template("index.html", headline="Tic Tac Toe Game")


@bp.route("/game", methods=["GET", "POST"])
def game() -> Union[str, Response]:
    """Shows the current game."""
    current_game = session["game"]
    board = current_game.board
    player = current_game.players_match.current()
    chosen_cell = None

    if "choice" in request.form:
        row_str, col_str = request.form["choice"].split()
        chosen_cell = int(row_str), int(col_str)
        board.set_cell(coord=chosen_cell, value=player.get_mark())
        current_game.players_match.switch()

        if not board.is_full() and not board.is_winning_move(
            chosen_cell, player.get_mark()
        ):
            player = current_game.players_match.current()
            chosen_cell = current_game.get_move()
            board.set_cell(coord=chosen_cell, value=player.get_mark())
            current_game.players_match.switch()

    if chosen_cell is None:
        pass
    elif board.is_winning_move(chosen_cell, player.get_mark()):
        player.record_win()
        return redirect(url_for("main.win", mark=player.display_mark()))
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
        "game.html",
        board=board.display(),
        turn=player.display_mark(),
        session=session,
        scores=current_game.get_scores(),
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


@bp.route("/multi_game/<string:room>")
def multi_game(room: str) -> str:
    """Initializes a new game."""
    print(room)
    return render_template("multi_game.html")


@bp.route("/join_game", methods=["GET", "POST"])
def join_game() -> Union[str, Response]:
    """Initializes a new game."""
    form = JoinMultiGame()
    if form.validate_on_submit():
        flash(f"Join multi game: {form.game_name.data}")
        print(form.game_name.data)
        return redirect(url_for("main.multi_game", room=form.game_name.data))
    return render_template("join_game.html", form=form)


@bp.route("/new_multi_game", methods=["GET", "POST"])
def new_multi_game() -> Union[str, Response]:
    """Initializes a new game."""
    form = CreateMultiGame()
    if form.validate_on_submit():
        flash(f"New multi game requested: {form.game_name.data}")
        print(form.game_name.data)
        return redirect(url_for("main.multi_game", room=form.game_name.data))
    return render_template("new_multi_game.html", form=form)


@bp.route("/move", methods=["POST"])
def move():
    """Processes a player's move."""
    player_move = request.form.get("move")

    print("/move")
    print(request.form)

    current_game = session["game"]
    board = current_game.board
    player = current_game.players_match.current()

    row_str, col_str = player_move.split()
    chosen_cell = int(row_str), int(col_str)
    board.set_cell(coord=chosen_cell, value=player.get_mark())
    current_game.players_match.switch()

    if not board.is_full() and not board.is_winning_move(
        chosen_cell, player.get_mark()
    ):
        player = current_game.players_match.current()
        chosen_cell = current_game.get_move()
        board.set_cell(coord=chosen_cell, value=player.get_mark())
        current_game.players_match.switch()

    if chosen_cell is None:
        pass
    elif board.is_winning_move(chosen_cell, player.get_mark()):
        player.record_win()
        return redirect(url_for("main.win", mark=player.display_mark()))
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
        "board.html", board=board.display(), turn=player.display_mark(), session=session
    )


@socketio.on("join")
def on_join(data):
    """TODO."""
    username = data["username"]
    room = data["room"]
    join_room(room)
    send(username + " has entered the room.", to=room)


@socketio.on("leave")
def on_leave(data):
    """TODO."""
    username = data["username"]
    room = data["room"]
    leave_room(room)
    send(username + " has left the room.", to=room)
