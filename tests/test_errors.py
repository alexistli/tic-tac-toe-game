"""Test cases for the errors module."""
import random

import pytest

from tic_tac_toe_game.errors import OverwriteCellError
from tic_tac_toe_game.errors import OverwriteCellError2


RANDOM_ROW = random.randint(0, 2)
RANDOM_COL = random.randint(0, 2)
RANDOM_COORD = (RANDOM_ROW, RANDOM_COL)

print(OverwriteCellError2(RANDOM_COORD))

def test_a():
    print(OverwriteCellError2(RANDOM_COORD))

# def test_overwrite_cell_error_raises() -> None:
#     """It raises a NotAvailableCellError exception."""
#     with pytest.raises(OverwriteCellError):
#         raise OverwriteCellError(RANDOM_COORD)


# def test_overwrite_cell_error_prints_info() -> None:
#     """It prints information about coord and value."""
#     with pytest.raises(OverwriteCellError) as exc:
#         raise OverwriteCellError(RANDOM_COORD)
#     assert exc.value.coord == RANDOM_COORD
#     assert str(exc.value) == f"Overwriting a non-empty cell is not allowed: cell at {RANDOM_COORD}"
#     # assert exc.value.__str__ == f"Overwriting a non-empty cell is not allowed: cell at {RANDOM_COORD}"
#
#
# def test_overwrite_cell_error_prints() -> None:
#     """It prints information about coord and value."""
#     exc = OverwriteCellError(RANDOM_COORD)
#     assert str(exc) == f"Overwriting a non-empty cell is not allowed: cell at {RANDOM_COORD}"
#     assert exc.__str__() == f"Overwriting a non-empty cell is not allowed: cell at {RANDOM_COORD}"
