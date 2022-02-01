"""Error classes used in the project."""
from typing import Sequence


Coordinates = Sequence[int]


class OverwriteCellError(Exception):
    """Raised when player tries to overwrite a non-empty cell."""

    def __init__(self, coord: Coordinates) -> None:
        """Constructor.

        Args:
            coord: tuple(int, int), the cell's coordinates.
        """
        msg = f"Overwriting a non-empty cell is not allowed: cell at {coord}"
        super().__init__(msg)
