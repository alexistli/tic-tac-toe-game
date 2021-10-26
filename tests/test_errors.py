"""Test cases for the errors module."""

# Standard library imports
import random

# Third-party imports
import pytest

# Local imports
from tic_tac_toe_game.errors import NotAvailableCellError


RANDOM_ROW = random.randint(0, 2)
RANDOM_COL = random.randint(0, 2)
RANDOM_COORD = (RANDOM_ROW, RANDOM_COL)


def test_not_available_cell_error_raises() -> None:
    """It raises a NotAvailableCellError exception."""
    with pytest.raises(NotAvailableCellError):
        exc = NotAvailableCellError(RANDOM_COORD)
        raise exc


def test_not_available_cell_error_prints_info() -> None:
    """It prints information about coord and value."""
    with pytest.raises(NotAvailableCellError):
        exc = NotAvailableCellError(RANDOM_COORD)
        raise exc
    assert str(RANDOM_COORD) in str(exc.coord)

