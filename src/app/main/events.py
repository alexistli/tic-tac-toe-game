"""Socket-IO events."""
import structlog
from flask import session
from flask_socketio import emit
from flask_socketio import join_room

from app import socketio
from tic_tac_toe_game import engine
from tic_tac_toe_game import state

logger = structlog.get_logger()


@socketio.event
def join(message):
    """TODO."""
    room = message["room"]
    join_room(room)
    session["room"] = room
    logger.info(f"Player joined room {room}", message=message)


@socketio.event
def move_received(data):
    """TODO."""
    logger.debug("move_received with data", data=data)

    current_game = state.get_state(data["room"])
    current_game.board.make_move(engine.Move(**data["move"]))
    current_game.players_match.switch()
    state.set_state(data["room"], current_game)

    emit(
        "refresh_game",
        to=data["room"],
        include_self=True,
    )
