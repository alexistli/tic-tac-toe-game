"""Error classes used in the project."""


class NotAvailableCellError(Exception):
    """Raised when player tries to set a non-empty cell."""

    def __init__(self, coord):
        """Constructor.

        Args:
            coord: tuple(int, int), the cell's coordinates.
        """
        self.coord = coord

    def __str__(self):
        """Returns message about exception."""
        return f"Cell at {self.coord} is not empty! You are not allowed to modify it."
