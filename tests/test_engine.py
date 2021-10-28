"""Test cases for the game module."""
import random

import pytest

from tic_tac_toe_game import engine
from tic_tac_toe_game import errors


PLAYER_NAME = "Sapiens"
PLAYER_A_NAME = "U-Man"
PLAYER_B_NAME = "Botybot"

PLAYER = engine.Player(PLAYER_NAME)
PLAYER_A = engine.HumanPlayer(PLAYER_A_NAME)
PLAYER_B = engine.AIPlayer(PLAYER_B_NAME)

MARK_X = "X"
MARK_O = "O"

RANDOM_ROW = random.randint(0, 2)
RANDOM_COL = random.randint(0, 2)
RANDOM_COORD = (RANDOM_ROW, RANDOM_COL)

FULL_GRID_LOOSE = "XOXOOXXXO"

# X would win turns 7 and 9 if this grid si filled in the read direction.
WIN_X_MOVES = ((2, 0), (2, 2))
WIN_X_GRID = "XOXOXOXOX"

# O would win turns 7 and 9 if this grid si filled in the read direction.
WIN_O_MOVES = ((2, 2),)
WIN_O_GRID = "OXXXOXOXO"


def load_grid(grid_str: str) -> engine.Grid:
    """Returns a Grid instance by loading a grid passed as a string."""
    n = 3
    matrix = [list(grid_str[i : i + n]) for i in range(0, len(grid_str), n)]
    grid = engine.Grid()
    grid.grid = matrix
    return grid


# ================ Test Grid ================


def test_grid_init_succeeds() -> None:
    """It returns an empty grid."""
    empty_grid = [[engine.Grid._empty_cell] * 3] * 3
    grid = engine.Grid()
    assert grid.grid == empty_grid


def test_grid_frame_succeeds() -> None:
    """It returns a framed grid."""
    data_row_str = engine.Grid._vertical_separator.join([engine.Grid._empty_cell] * 3)
    separator_row_str = engine.Grid._intersection.join(
        [engine.Grid._horizontal_separator] * 3
    )
    framed_grid = ("\n" + separator_row_str + "\n").join([data_row_str] * 3)

    grid = engine.Grid()
    assert grid.framed_grid() == framed_grid


def test_grid_handles_cell_operations() -> None:
    """It handles cell operations."""
    grid = engine.Grid()
    for row_index, row in enumerate(grid.grid):
        for col_index, _cell in enumerate(row):
            coord = (row_index, col_index)
            assert grid.is_empty_cell(coord) is True
            grid.set_cell(coord, MARK_X)
            assert grid.get_cell(coord) == MARK_X
            assert grid.is_empty_cell(coord) is False


def test_grid_handles_cell_override() -> None:
    """It handles cell overriding attempt."""
    grid = engine.Grid()
    assert grid.is_empty_cell(RANDOM_COORD) is True
    grid.set_cell(RANDOM_COORD, MARK_X)
    assert grid.get_cell(RANDOM_COORD) == MARK_X
    with pytest.raises(errors.OverwriteCellError):
        grid.set_cell(RANDOM_COORD, MARK_O)
        assert grid.get_cell(RANDOM_COORD) == MARK_X


def test_not_full_grid_returns_is_not_full() -> None:
    """It returns False when grid is not full."""
    # grid is empty
    grid = engine.Grid()
    assert grid.is_full() is False

    # grid is neither empty nor full
    for mark in (MARK_X, MARK_O):
        grid = engine.Grid()
        for row_index, row in enumerate(grid.grid):
            for col_index, _cell in enumerate(row):
                assert grid.is_full() is False
                grid.set_cell((row_index, col_index), mark)


def test_full_grid_returns_is_full() -> None:
    """It returns True when grid is full."""
    full_grid = load_grid(FULL_GRID_LOOSE)
    assert full_grid.is_full() is True

    for mark in (MARK_X, MARK_O):
        grid = engine.Grid()
        for row_index, row in enumerate(grid.grid):
            for col_index, _cell in enumerate(row):
                grid.set_cell((row_index, col_index), mark)
        assert grid.is_full() is True


def test_not_is_winning_move() -> None:
    """It returns False if move is not a winning move."""
    loose_grid = load_grid(FULL_GRID_LOOSE)
    grid = engine.Grid()
    # Transfers all cells from loosing_grid to the new grid.
    # Every move should be a loosing move.
    for row_index, row in enumerate(grid.grid):
        for col_index, _cell in enumerate(row):
            coord = (row_index, col_index)
            mark = loose_grid.get_cell(coord)
            grid.set_cell(coord, mark)
            assert grid.is_winning_move(coord, mark) is False


def test_is_winning_move() -> None:
    """It returns True if move is a winning move."""
    for win_grid, win_moves in ((WIN_X_GRID, WIN_X_MOVES), (WIN_O_GRID, WIN_O_MOVES)):
        model_grid = load_grid(win_grid)
        grid = engine.Grid()
        # Transfers all cells from loosing_grid to the new grid.
        # Every move should be a loosing move.
        for row_index, row in enumerate(grid.grid):
            for col_index, _cell in enumerate(row):
                coord = (row_index, col_index)
                mark = model_grid.get_cell(coord)
                grid.set_cell(coord, mark)
                is_winning = bool(coord in win_moves)
                assert bool(grid.is_winning_move(coord, mark)) == is_winning


def test_returns_random_available_cell_succeeds() -> None:
    """It returns a random available cell."""
    grid = engine.Grid()
    for _ in range(0, 9):
        value = random.choice((MARK_X, MARK_O))
        cell = grid.random_available_cell()
        assert grid.is_empty_cell(cell) is True
        grid.set_cell(cell, value)
    assert grid.is_full() is True


def test_handles_random_available_cell_exception() -> None:
    """It raises `IndexError` if grid is full."""
    grid = load_grid(FULL_GRID_LOOSE)
    with pytest.raises(IndexError) as exc:
        grid.random_available_cell()
    assert "Grid is full" in str(exc.value)


# ================ Test Player ================


def test_player_handles_mark() -> None:
    """It handles get and set for marks."""
    for player in (
        engine.Player(PLAYER_NAME),
        engine.HumanPlayer(PLAYER_A_NAME),
        engine.AIPlayer(PLAYER_B_NAME),
    ):
        assert player.get_mark() is None
        player.set_mark(MARK_X)
        assert player.get_mark() == MARK_X
        player.set_mark(MARK_O)
        assert player.get_mark() == MARK_O


def test_player_returns_repr() -> None:
    """It returns expected repr."""
    player = engine.Player(PLAYER_NAME)
    player_a = engine.HumanPlayer(PLAYER_A_NAME)
    player_b = engine.AIPlayer(PLAYER_B_NAME)

    assert repr(player) == f"Player({repr(PLAYER_NAME)}, None)"
    player.set_mark(MARK_X)
    assert repr(player) == f"Player({repr(PLAYER_NAME)}, {repr(MARK_X)})"

    assert repr(player_a) == f"HumanPlayer({repr(PLAYER_A_NAME)}, None)"
    player_a.set_mark(MARK_X)
    assert repr(player_a) == f"HumanPlayer({repr(PLAYER_A_NAME)}, {repr(MARK_X)})"

    assert repr(player_b) == f"AIPlayer({repr(PLAYER_B_NAME)}, None)"
    player_b.set_mark(MARK_O)
    assert repr(player_b) == f"AIPlayer({repr(PLAYER_B_NAME)}, {repr(MARK_O)})"


# ================ Test Game ================


def test_game_inits() -> None:
    """It inits and returns expected attribute values."""
    player_a = engine.HumanPlayer(PLAYER_A_NAME)
    player_b = engine.AIPlayer(PLAYER_B_NAME)
    game = engine.Game(player_a, player_b)
    assert game.player_x == player_a
    assert game.player_o == player_b
    assert game.current_player == player_a
    assert isinstance(game.grid, engine.Grid)


def test_game_handles_player_get_and_switch() -> None:
    """It handles current player get and switch."""
    player_a = engine.HumanPlayer(PLAYER_A_NAME)
    player_b = engine.AIPlayer(PLAYER_B_NAME)
    game = engine.Game(player_a, player_b)
    assert game.current_player == player_a
    assert game.get_player() == player_a
    game.switch_player()
    assert game.current_player == player_b
    assert game.get_player() == player_b
    game.switch_player()
    assert game.current_player == player_a
    assert game.get_player() == player_a


def test_game_returns_repr() -> None:
    """It returns expected repr."""
    player_a = engine.HumanPlayer(PLAYER_A_NAME)
    player_b = engine.AIPlayer(PLAYER_B_NAME)
    grid = engine.Grid()
    game = engine.Game(player_a, player_b)

    assert repr(game) == (
        f"Game({repr(player_a)}, {repr(player_b)}, " f"{repr(player_a)}, {repr(grid)})"
    )
