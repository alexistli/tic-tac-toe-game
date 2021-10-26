"""Test cases for the game module."""
# Standard library imports
# Third-party imports
from tic_tac_toe_game.game import Grid
from tic_tac_toe_game.game import Player

# Local imports


def test_grid_init_succeeds() -> None:
    """It returns an empty grid."""
    empty_grid = [[Grid._empty_cell] * 3] * 3
    grid: Grid = Grid()
    assert grid.grid == empty_grid
    assert Grid._empty_grid == empty_grid


def test_grid_frame_succeeds() -> None:
    """It returns a framed grid."""
    data_row_str = Grid._vertical_separator.join([Grid._empty_cell] * 3)
    separator_row_str = Grid._intersection.join([Grid._horizontal_separator] * 3)
    framed_grid = ("\n" + separator_row_str + "\n").join([data_row_str] * 3)

    grid: Grid = Grid()
    assert grid.framed_grid() == framed_grid


def test_player_handles_mark() -> None:
    """It handles get and set for marks."""
    mark = "X"
    player = Player("Alexis")
    assert player.get_mark() is None
    player.set_mark(mark)
    assert player.get_mark() == mark
