"""Flask app routes."""
import uuid
from typing import Union

import structlog
from flask import current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import session
from flask import url_for
from werkzeug import Response

from app.main import bp
from app.main.forms import CreateMultiGame
from app.main.forms import JoinMultiGame
from tic_tac_toe_game import engine
from tic_tac_toe_game.AI import mcts
from tic_tac_toe_game.AI import naive
from tic_tac_toe_game.AI import negamax

logger = structlog.get_logger()


@bp.before_request
def before_request_func():
    """Prepares the structlog logger before each request.

    Each request will have its own `request_id` to help debugging.
    """
    structlog.threadlocal.clear_threadlocal()
    structlog.threadlocal.bind_threadlocal(
        view=request.path,
        request_id=str(uuid.uuid4()),
        peer=request.access_route[0],
    )


@bp.app_errorhandler(404)
def not_found_error(_):
    """Handles 404 not found error."""
    return render_template("404.html"), 404


@bp.app_errorhandler(500)
def internal_error(_):
    """Handles 500 internal error."""
    return render_template("500.html"), 500


@bp.route("/static/<path:filename>")
def staticfiles(filename):
    """Serving static files."""
    return send_from_directory(current_app.config["STATIC_FOLDER"], filename)


@bp.route("/session", methods=["GET"])
def session_view():
    """Display session variable value."""
    return render_template("session.html", session_variables=str(session))


@bp.route("/")
def index() -> str:
    """Shows the website index."""
    logger.info("in index")

    log = logger.bind()
    log.info("user on index page", user="test-user")

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
    logger.debug(
        f"game - game.players_match.players: {current_game.players_match.players}"
    )

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
    logger.debug(f"multi_game - session: {session}")
    current_game = session["game"]
    board = current_game.board
    player = current_game.players_match.current()

    return render_template(
        "game_multi.html",
        board=board.display(),
        turn=player.display_mark(),
        my_mark=session["my_mark"],
        scores=current_game.get_scores(),
        room=room,
    )


@bp.route("/join_game", methods=["GET", "POST"])
def join_game() -> Union[str, Response]:
    """Initializes a new game."""
    form = JoinMultiGame()
    logger.info("join_game")
    logger.debug("join_game")

    if form.validate_on_submit():
        flash(f"Join multi game: {form.game_name.data}")
        logger.debug(f"join_game - form.game_name.data: {form.game_name.data}")

        current_game = engine.build_game(mode="multi")
        session["game"] = current_game
        current_game.players_match.switch()
        session["my_id"] = current_game.players_match.current().get_mark()
        session["my_mark"] = current_game.players_match.current().display_mark()
        current_game.players_match.switch()

        logger.debug(f"join_game - session: {session}")

        return redirect(url_for("main.multi_game", room=form.game_name.data))
    return render_template("join_game.html", form=form)


@bp.route("/new_multi_game", methods=["GET", "POST"])
def new_multi_game() -> Union[str, Response]:
    """Initializes a new game."""
    form = CreateMultiGame()
    if form.validate_on_submit():
        flash(f"New multi game requested: {form.game_name.data}")
        logger.debug(f"new_multi_game - form.game_name.data: {form.game_name.data}")

        current_game = engine.build_game(mode="multi")
        session["game"] = current_game
        session["my_id"] = current_game.players_match.current().get_mark()
        session["my_mark"] = current_game.players_match.current().display_mark()

        logger.debug(f"new_multi_game - session: {session}")

        return redirect(url_for("main.multi_game", room=form.game_name.data))
    return render_template("new_multi_game.html", form=form)


@bp.route("/move_multi", methods=["POST"])
def move_multi():
    """Processes a player's move."""
    player_move = request.form.get("coord")

    logger.debug(f"move_multi - request.form: {request.form}")

    current_game = session["game"]
    board = current_game.board
    player = current_game.players_match.current()

    row_str, col_str = player_move.split()
    logger.debug(f"row_str, col_str: {row_str} {col_str}")
    chosen_cell = int(row_str), int(col_str)
    logger.debug(f"chosen_cell: {chosen_cell}")
    board.set_cell(coord=chosen_cell, value=player.get_mark())

    if board.is_winning_move(chosen_cell, player.get_mark()):
        player.record_win()
        return redirect(url_for("main.win", mark=player.display_mark()))
    elif board.is_full():
        return redirect(url_for("main.tie"))

    current_game.players_match.switch()
    player = current_game.players_match.current()

    return render_template(
        "board_multi.html", board=board.display(), turn=player.display_mark()
    )


@bp.route("/board", methods=["GET"])
def board():
    """Returns the current board state."""
    current_game = session["game"]
    current_board = current_game.board
    current_player = current_game.players_match.current()
    logger.debug("game retrieved from session", game=current_game, session=session)

    # if board.is_winning_move(chosen_cell, player.get_mark()):
    #     player.record_win()
    #     return redirect(url_for("main.win", mark=player.display_mark()))
    # elif board.is_full():
    #     return redirect(url_for("main.tie"))

    return render_template(
        "board_multi.html",
        board=current_board.display(),
        turn=current_player.display_mark(),
    )


@bp.route("/move", methods=["POST"])
def move():
    """Processes a player's move."""
    player_move = request.form.get("move")

    logger.debug(f"move - request.form: {request.form}")

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
    logger.debug(
        f"move - game.players_match.players: {current_game.players_match.players}"
    )

    return render_template(
        "board.html", board=board.display(), turn=player.display_mark(), session=session
    )
