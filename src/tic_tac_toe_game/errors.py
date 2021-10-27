"""Error classes used in the project."""
from typing import Optional
from typing import Tuple


class OverwriteCellError(Exception):  # pragma: no cover
    """Raised when player tries to overwrite a non-empty cell."""

    def __init__(self, coord: Tuple[int, int]) -> None:
        """Constructor.

        Args:
            coord: tuple(int, int), the cell's coordinates.
        """
        msg = f"Overwriting a non-empty cell is not allowed: cell at {coord}"
        super(OverwriteCellError, self).__init__(msg)
