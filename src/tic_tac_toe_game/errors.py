"""Error classes used in the project."""
from typing import Tuple


class GameException(Exception):  # pragma: no cover
    """Base Exception class for all the classes of this project."""


class OverwriteCellError(GameException):
    """Raised when player tries to overwrite a non-empty cell."""

    def __init__(self, coord: Tuple[int, int]) -> None:  # pragma: no cover
        """Constructor.

        Args:
            coord: tuple(int, int), the cell's coordinates.
        """
        msg = f"Overwriting a non-empty cell is not allowed: cell at {coord}"
        super(OverwriteCellError, self).__init__(msg)
