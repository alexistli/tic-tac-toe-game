"""Error classes used in the project."""
from typing import Tuple, Optional


class OverwriteCellError(Exception):  # pragma: no cover
    """Raised when player tries to overwrite a non-empty cell."""

    def __init__(self, coord: Tuple[int, int]) -> None:
        """Constructor.

        Args:
            coord: tuple(int, int), the cell's coordinates.
        """
        msg = f"Overwriting a non-empty cell is not allowed: cell at {coord}"
        super(OverwriteCellError, self).__init__(msg)


class NotAvailableError(Exception):  # pragma: no cover
    """Raised when conditions, to perform an operation, are not available."""

    def __init__(self, message: Optional[str] = None) -> None:
        """Constructor.

        Args:
            message: str, additional information about the error.
        """
        msg = f"Operation can't be performed as conditions are not available"
        if message is not None:
            msg += f": {message}"
        super(NotAvailableError, self).__init__(msg)
