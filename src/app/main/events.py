"""Socket-IO events."""
from typing import Tuple

import structlog
from flask import session
from flask_socketio import close_room
from flask_socketio import emit
from flask_socketio import join_room
from flask_socketio import leave_room
from flask_socketio import rooms

from app import socketio
from tic_tac_toe_game import engine

logger = structlog.get_logger()


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
def move_received(data):
    """TODO."""
    logger.debug(f"socket.move: {data}")
    chosen_cell = parse_raw_move(data["coord"])

    current_game = session["game"]
    logger.debug("before persist_move", game=current_game)

    current_mark = current_game.players_match.current().get_mark()
    current_game.board.set_cell(coord=chosen_cell, value=current_mark)
    current_game.players_match.switch()
    session["game"] = current_game

    logger.debug("after persist_move", game=current_game, session=session)

    emit(
        "sync_move",
        {"chosen_cell": chosen_cell},
        broadcast=True,
    )
    emit(
        "refresh_game",
        to=data["room"],
        include_self=True,
    )


@socketio.event
def sync_move(data):
    """TODO."""
    logger.debug(f"socket.sync_move: {data}")
    chosen_cell = data["coord"]

    current_game = session["game"]
    logger.debug("before persist_move", game=current_game)

    current_mark = current_game.players_match.current().get_mark()
    current_game.board.set_cell(coord=chosen_cell, value=current_mark)
    current_game.players_match.switch()
    session["game"] = current_game

    logger.debug("after persist_move", game=current_game, session=session)


@socketio.event
def receive_move(data):
    """TODO."""
    logger.debug(f"socket.receive_move: {data}")

    player_move = data["coord"]

    logger.debug(f"player_move: {player_move}")

    current_game = session["game"]
    current_player = current_game.players_match.current()

    row_str, col_str = player_move.split()
    logger.debug(f"row_str, col_str: {row_str} {col_str}")
    chosen_cell = int(row_str), int(col_str)
    logger.debug(f"chosen_cell: {chosen_cell}")
    current_game.board.set_cell(coord=chosen_cell, value=current_player.get_mark())

    current_game.players_match.switch()

    emit(
        "refresh_game",
        to=data["room"],
        include_self=False,
    )


def parse_raw_move(raw_move: str) -> Tuple[int, int]:
    """TODO."""
    logger.debug(f"raw_move: {raw_move}")
    row_str, col_str = raw_move.split()
    logger.debug(f"row_str, col_str: {row_str} {col_str}")
    parsed_move = int(row_str), int(col_str)
    return parsed_move


def persist_move(game: engine.Engine, cell: Tuple[int, int]) -> None:
    """TODO."""
    logger.debug("before persist_move", game=game)

    current_mark = game.players_match.current().get_mark()
    game.board.set_cell(coord=cell, value=current_mark)
    game.players_match.switch()

    logger.debug("after persist_move", game=game, session=session)
