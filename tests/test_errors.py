"""Test cases for the errors module."""
import random

import pytest
from pytest_mock import MockFixture
from unittest.mock import Mock


from tic_tac_toe_game.errors import OverwriteCellError, GameException

RANDOM_ROW = random.randint(0, 2)
RANDOM_COL = random.randint(0, 2)
RANDOM_COORD = (RANDOM_ROW, RANDOM_COL)


@pytest.fixture
def mock_exception_init(mocker: MockFixture) -> Mock:
    """Fixture for mocking Exception class."""
    return mocker.patch("tic_tac_toe_game.errors.GameException.__init__")


def test_overwrite_cell_error_raises() -> None:
    """It raises a OverwriteCellError exception."""
    with pytest.raises(OverwriteCellError) as exc:
        raise OverwriteCellError(RANDOM_COORD)
    assert str(exc.value) == f"Overwriting a non-empty cell is not allowed: cell at {RANDOM_COORD}"
    assert "OverwriteCellError" in repr(exc.value)


def test_overwrite_cell_error_super(mock_exception_init: Mock) -> None:
    """It raises a OverwriteCellError exception."""
    exc = OverwriteCellError(RANDOM_COORD)
    mock_exception_init.assert_called_with(
        f"Overwriting a non-empty cell is not allowed: cell at {RANDOM_COORD}"
    )


def test_overwrite_cell_error_is_subclass() -> None:
    """It is instance of BaseException."""
    exc = OverwriteCellError(RANDOM_COORD)
    assert isinstance(exc, GameException)
    assert issubclass(OverwriteCellError, GameException)

# def test_overwrite_cell_error_super(mocker: Mock) -> None:
#     """It raises a OverwriteCellError exception."""
#     mocker.patch("__main__.__builtins__.Exception.__init__")
#     exc = OverwriteCellError(RANDOM_COORD)
#     Exception.__init__.assert_called_once_with('file')
