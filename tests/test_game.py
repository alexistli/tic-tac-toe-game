"""Test cases for the game module."""
# Standard library imports
# Third-party imports
from tic_tac_toe_game.game import AIPlayer
from tic_tac_toe_game.game import Game
from tic_tac_toe_game.game import Grid
from tic_tac_toe_game.game import HumanPlayer
from tic_tac_toe_game.game import Player

# Local imports


PLAYER_A = HumanPlayer("U-Man")
PLAYER_B = AIPlayer("Botybot")


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
    mark_x = "X"
    mark_o = "O"
    players = (Player("Alexis"), HumanPlayer("U-Man"), AIPlayer("Botybot"))
    for player in players:
        assert player.get_mark() is None
        player.set_mark(mark_x)
        assert player.get_mark() == mark_x
        player.set_mark(mark_o)
        assert player.get_mark() == mark_o


def test_game_inits() -> None:
    """It inits and returns expected attribute values."""
    game = Game(PLAYER_A, PLAYER_B)
    assert game.player_x == PLAYER_A
    assert game.player_o == PLAYER_B
    assert game.current_player == PLAYER_A
    assert isinstance(game.grid, Grid)


def test_game_handles_player_get_and_switch() -> None:
    """It handles current player get and switch."""
    game = Game(PLAYER_A, PLAYER_B)
    assert game.current_player == PLAYER_A
    assert game.get_player() == PLAYER_A
    game.switch_player()
    assert game.current_player == PLAYER_B
    assert game.get_player() == PLAYER_B
    game.switch_player()
    assert game.current_player == PLAYER_A
    assert game.get_player() == PLAYER_A
