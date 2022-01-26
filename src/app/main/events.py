"""Socket-IO events."""
from typing import Tuple

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
    logger.debug(f"socket.move: {data}")
    chosen_cell = parse_raw_move(data["coord"])

    room = session["room"]
    current_game = state.get_state(room)
    logger.debug("before persist_move", game=current_game)

    current_mark = current_game.players_match.current().get_mark()
    current_game.board.set_cell(coord=chosen_cell, value=current_mark)
    current_game.players_match.switch()

    state.set_state(room, current_game)

    emit(
        "refresh_game",
        to=data["room"],
        include_self=True,
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
