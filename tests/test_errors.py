"""Test cases for the errors module."""
import random

import pytest

from tic_tac_toe_game import errors


RANDOM_ROW = random.randint(0, 2)
RANDOM_COL = random.randint(0, 2)
RANDOM_COORD = (RANDOM_ROW, RANDOM_COL)


def test_overwrite_cell_error_raises() -> None:
    """It raises a OverwriteCellError exception."""
    with pytest.raises(errors.OverwriteCellError) as exc:
        raise errors.OverwriteCellError(RANDOM_COORD)
    assert (
        str(exc.value)
        == f"Overwriting a non-empty cell is not allowed: cell at {RANDOM_COORD}"
    )
    assert "OverwriteCellError" in repr(exc.value)
