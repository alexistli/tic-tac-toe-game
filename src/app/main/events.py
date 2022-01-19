"""Socket-IO events."""
from flask import session
from flask_socketio import close_room
from flask_socketio import emit
from flask_socketio import join_room
from flask_socketio import leave_room
from flask_socketio import rooms

from app import socketio
from app.main.routes import board
from app.main.routes import logger


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
