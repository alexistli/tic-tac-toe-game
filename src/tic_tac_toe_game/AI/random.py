"""Implementation of a random cell picking algorithm for Tic Tac Toe Game."""
import random
from typing import Tuple

from tic_tac_toe_game.engine import Board


def random_move(board: Board, *args: str) -> Tuple[int, int]:
    """Returns a randomly picked cell among available cells."""
    empty_cells = [
        (row_id, col_id)
        for row_id, row in enumerate(board.grid)
        for col_id, cell in enumerate(row)
        if board.is_empty_cell((row_id, col_id))
    ]
    try:
        random_cell = random.choice(empty_cells)
    except IndexError:
        raise IndexError("Grid is full, cannot choose an available cell") from None
    return random_cell
