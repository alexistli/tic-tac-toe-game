"""Implementation of a random cell picking algorithm for Tic Tac Toe Game."""
import random
from typing import List
from typing import Tuple


def naive_move(grid: List[List[int]], *args: int) -> Tuple[int, int]:
    """Returns a randomly picked cell among available cells."""
    print(grid)
    print(args)
    empty_cells = [
        (row_id, col_id)
        for row_id, row in enumerate(grid)
        for col_id, cell in enumerate(row)
        if cell == 0
    ]
    try:
        random_cell = random.choice(empty_cells)
    except IndexError:
        raise IndexError("Grid is full, cannot choose an available cell") from None
    return random_cell
