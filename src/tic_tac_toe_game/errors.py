"""Error classes used in the project."""
from typing import Tuple


class OverwriteCellError(Exception):
    """Raised when player tries to set a non-empty cell."""

    def __init__(self, coord: Tuple[int, int]) -> None:
        """Constructor.

        Args:
            coord: tuple(int, int), the cell's coordinates.
        """
        self.coord = coord

    def __str__(self) -> str:
        """Returns message about exception."""
        return f"Overwriting a non-empty cell is not allowed: cell at {self.coord}"


class OverwriteCellError2(Exception):
    """Raised when player tries to set a non-empty cell."""

    def __init__(self, coord: Tuple[int, int]) -> None:
        msg = f"Overwriting a non-empty cell is not allowed: cell at {coord}"
        super(OverwriteCellError2, self).__init__(msg)
