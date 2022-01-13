"""Flask app routes."""
from typing import Union

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_socketio import close_room
from flask_socketio import emit
from flask_socketio import join_room
from flask_socketio import leave_room
from flask_socketio import rooms
from werkzeug import Response

from app import logger
from app import socketio
from app.main import bp
from app.main.forms import CreateMultiGame
from app.main.forms import JoinMultiGame
from tic_tac_toe_game import engine
from tic_tac_toe_game.AI import mcts
from tic_tac_toe_game.AI import naive
from tic_tac_toe_game.AI import negamax


@bp.route("/session", methods=["GET"])
def session_view():
    """Display session variable value."""
    return render_template("session.html", session_variables=str(session))


@bp.route("/")
def index() -> str:
    """Shows the website index."""
    # log = logger.bind()
    # log.info("user on index page", user="test-user")
    logger.info("in index")
    # a = session["a"]
    # b = session["b"]
    # c = session["c"]

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


@socketio.event
def join(message):
    """TODO."""
    join_room(message["room"])
    logger.debug(f"room joined: {message}")
    session["receive_count"] = session.get("receive_count", 0) + 1
    logger.debug("emit my_response")
    emit(
        "my_response",
        {"data": "In rooms: " + ", ".join(rooms()), "count": session["receive_count"]},
    )

    logger.debug("emit my_room_event")
    emit("my_room_event", {"room": message["room"], "data": message["room"]})


@socketio.event
def leave(message):
    """TODO."""
    leave_room(message["room"])
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": "In rooms: " + ", ".join(rooms()), "count": session["receive_count"]},
    )


@socketio.on("close_room")
def on_close_room(message):
    """TODO."""
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {
            "data": "Room " + message["room"] + " is closing.",
            "count": session["receive_count"],
        },
        to=message["room"],
    )
    close_room(message["room"])


@socketio.event
def my_room_event(message):
    """TODO."""
    logger.debug(f"my_room_event: {message}")
    session["receive_count"] = session.get("receive_count", 0) + 1
    emit(
        "my_response",
        {"data": message["data"], "count": session["receive_count"]},
        to=message["room"],
        include_self=False,
    )


@socketio.event
def emit_move(data):
    """TODO."""
    logger.debug(f"socket.emit_move: {data}")
    emit(
        "receive_move",
        data,
        to=data["room"],
        include_self=True,
    )


@socketio.event
def receive_move(data):
    """TODO."""
    logger.debug(f"socket.receive_move: {data}")

    player_move = data["coord"]

    print("/receive_move")
    print(player_move)

    current_game = session["game"]
    current_player = current_game.players_match.current()

    row_str, col_str = player_move.split()
    logger.debug(f"row_str, col_str: {row_str} {col_str}")
    chosen_cell = int(row_str), int(col_str)
    logger.debug(f"chosen_cell: {chosen_cell}")
    board.set_cell(coord=chosen_cell, value=current_player.get_mark())

    current_game.players_match.switch()

    emit(
        "refresh_game",
        to=data["room"],
        include_self=False,
    )
