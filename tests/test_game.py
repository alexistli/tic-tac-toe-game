"""Test cases for the game module."""
import random

import pytest

from tic_tac_toe_game.errors import OverwriteCellError
from tic_tac_toe_game.game import AIPlayer
from tic_tac_toe_game.game import Game
from tic_tac_toe_game.game import Grid
from tic_tac_toe_game.game import HumanPlayer
from tic_tac_toe_game.game import Player


PLAYER_NAME = "Sapiens"
PLAYER_A_NAME = "U-Man"
PLAYER_B_NAME = "Botybot"

PLAYER = Player(PLAYER_NAME)
PLAYER_A = HumanPlayer(PLAYER_A_NAME)
PLAYER_B = AIPlayer(PLAYER_B_NAME)

MARK_X = "X"
MARK_O = "O"

RANDOM_ROW = random.randint(0, 2)
RANDOM_COL = random.randint(0, 2)
RANDOM_COORD = (RANDOM_ROW, RANDOM_COL)


def test_grid_init_succeeds() -> None:
    """It returns an empty grid."""
    empty_grid = [[Grid._empty_cell] * 3] * 3
    grid = Grid()
    assert grid.grid == empty_grid


def test_grid_frame_succeeds() -> None:
    """It returns a framed grid."""
    data_row_str = Grid._vertical_separator.join([Grid._empty_cell] * 3)
    separator_row_str = Grid._intersection.join([Grid._horizontal_separator] * 3)
    framed_grid = ("\n" + separator_row_str + "\n").join([data_row_str] * 3)

    grid = Grid()
    assert grid.framed_grid() == framed_grid


def test_grid_handles_cell_operations() -> None:
    """It handles cell operations."""
    grid = Grid()
    for row_index, row in enumerate(grid.grid):
        for col_index, _cell in enumerate(row):
            coord = (row_index, col_index)
            assert grid.is_empty_cell(coord)
            grid.set_cell(coord, MARK_X)
            assert grid.get_cell(coord) == MARK_X
            assert not grid.is_empty_cell(coord)


def test_grid_handles_cell_override() -> None:
    """It handles cell overriding attempt."""
    grid = Grid()
    assert grid.is_empty_cell(RANDOM_COORD) is True
    grid.set_cell(RANDOM_COORD, MARK_X)
    assert grid.get_cell(RANDOM_COORD) == MARK_X
    with pytest.raises(OverwriteCellError):
        grid.set_cell(RANDOM_COORD, MARK_O)
        assert grid.get_cell(RANDOM_COORD) == MARK_X


def test_player_handles_mark() -> None:
    """It handles get and set for marks."""
    for player in (
        Player(PLAYER_NAME),
        HumanPlayer(PLAYER_A_NAME),
        AIPlayer(PLAYER_B_NAME),
    ):
        assert player.get_mark() is None
        player.set_mark(MARK_X)
        assert player.get_mark() == MARK_X
        player.set_mark(MARK_O)
        assert player.get_mark() == MARK_O


def test_player_returns_repr() -> None:
    """It returns expected repr."""
    player = Player(PLAYER_NAME)
    player_a = HumanPlayer(PLAYER_A_NAME)
    player_b = AIPlayer(PLAYER_B_NAME)

    assert repr(player) == f"Player({repr(PLAYER_NAME)}, None)"
    player.set_mark(MARK_X)
    assert repr(player) == f"Player({repr(PLAYER_NAME)}, {repr(MARK_X)})"

    assert repr(player_a) == f"HumanPlayer({repr(PLAYER_A_NAME)}, None)"
    player_a.set_mark(MARK_X)
    assert repr(player_a) == f"HumanPlayer({repr(PLAYER_A_NAME)}, {repr(MARK_X)})"

    assert repr(player_b) == f"AIPlayer({repr(PLAYER_B_NAME)}, None)"
    player_b.set_mark(MARK_O)
    assert repr(player_b) == f"AIPlayer({repr(PLAYER_B_NAME)}, {repr(MARK_O)})"


def test_game_inits() -> None:
    """It inits and returns expected attribute values."""
    player_a = HumanPlayer(PLAYER_A_NAME)
    player_b = AIPlayer(PLAYER_B_NAME)
    game = Game(player_a, player_b)
    assert game.player_x == player_a
    assert game.player_o == player_b
    assert game.current_player == player_a
    assert isinstance(game.grid, Grid)


def test_game_handles_player_get_and_switch() -> None:
    """It handles current player get and switch."""
    player_a = HumanPlayer(PLAYER_A_NAME)
    player_b = AIPlayer(PLAYER_B_NAME)
    game = Game(player_a, player_b)
    assert game.current_player == player_a
    assert game.get_player() == player_a
    game.switch_player()
    assert game.current_player == player_b
    assert game.get_player() == player_b
    game.switch_player()
    assert game.current_player == player_a
    assert game.get_player() == player_a
