"""Test cases for the game module."""
import random

import pytest

from tic_tac_toe_game import engine
from tic_tac_toe_game import errors


PLAYER_NAME = "Sapiens"
PLAYER_A_NAME = "U-Man"
PLAYER_B_NAME = "Botybot"

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


def load_grid(grid_str: str) -> engine.Board:
    """Returns a Grid instance by loading a grid passed as a string."""
    n = 3
    matrix = [list(grid_str[i : i + n]) for i in range(0, len(grid_str), n)]
    grid = engine.Board()
    grid.grid = matrix
    return grid


# ================ Test Grid ================


def test_grid_init_succeeds() -> None:
    """It returns an empty grid."""
    empty_grid = [[engine.Board._empty_cell] * 3] * 3
    grid = engine.Board()
    assert grid.grid == empty_grid


def test_grid_frame_succeeds() -> None:
    """It returns a framed grid."""
    data_row_str = engine.Board._vertical_separator.join([engine.Board._empty_cell] * 3)
    separator_row_str = engine.Board._intersection.join(
        [engine.Board._horizontal_separator] * 3
    )
    framed_grid = ("\n" + separator_row_str + "\n").join([data_row_str] * 3)

    grid = engine.Board()
    assert grid.framed_grid() == framed_grid


def test_grid_handles_cell_operations() -> None:
    """It handles cell operations."""
    grid = engine.Board()
    for row_index, row in enumerate(grid.grid):
        for col_index, _cell in enumerate(row):
            coord = (row_index, col_index)
            assert grid.is_empty_cell(coord) is True
            grid.set_cell(coord, MARK_X)
            assert grid.get_cell(coord) == MARK_X
            assert grid.is_empty_cell(coord) is False


def test_grid_handles_cell_override() -> None:
    """It handles cell overriding attempt."""
    grid = engine.Board()
    assert grid.is_empty_cell(RANDOM_COORD) is True
    grid.set_cell(RANDOM_COORD, MARK_X)
    assert grid.get_cell(RANDOM_COORD) == MARK_X
    with pytest.raises(errors.OverwriteCellError):
        grid.set_cell(RANDOM_COORD, MARK_O)
        assert grid.get_cell(RANDOM_COORD) == MARK_X


def test_not_full_grid_returns_is_not_full() -> None:
    """It returns False when grid is not full."""
    # grid is empty
    grid = engine.Board()
    assert grid.is_full() is False

    # grid is neither empty nor full
    for mark in (MARK_X, MARK_O):
        grid = engine.Board()
        for row_index, row in enumerate(grid.grid):
            for col_index, _cell in enumerate(row):
                assert grid.is_full() is False
                grid.set_cell((row_index, col_index), mark)


def test_full_grid_returns_is_full() -> None:
    """It returns True when grid is full."""
    full_grid = load_grid(FULL_GRID_LOOSE)
    assert full_grid.is_full() is True

    for mark in (MARK_X, MARK_O):
        grid = engine.Board()
        for row_index, row in enumerate(grid.grid):
            for col_index, _cell in enumerate(row):
                grid.set_cell((row_index, col_index), mark)
        assert grid.is_full() is True


def test_not_is_winning_move() -> None:
    """It returns False if move is not a winning move."""
    loose_grid = load_grid(FULL_GRID_LOOSE)
    grid = engine.Board()
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
        grid = engine.Board()
        # Transfers all cells from loosing_grid to the new grid.
        # Every move should be a loosing move.
        for row_index, row in enumerate(grid.grid):
            for col_index, _cell in enumerate(row):
                coord = (row_index, col_index)
                mark = model_grid.get_cell(coord)
                grid.set_cell(coord, mark)
                is_winning = bool(coord in win_moves)
                assert bool(grid.is_winning_move(coord, mark)) == is_winning


@pytest.mark.xfail(reason="random_available_cell method was moved")
def test_returns_random_available_cell_succeeds() -> None:
    """It returns a random available cell."""
    grid = engine.Board()
    for _ in range(0, 9):
        value = random.choice((MARK_X, MARK_O))
        cell = grid.random_available_cell()
        assert grid.is_empty_cell(cell) is True
        grid.set_cell(cell, value)
    assert grid.is_full() is True


@pytest.mark.xfail(reason="random_available_cell method was moved")
def test_handles_random_available_cell_exception() -> None:
    """It raises `IndexError` if grid is full."""
    grid = load_grid(FULL_GRID_LOOSE)
    with pytest.raises(IndexError) as exc:
        grid.random_available_cell()
    assert "Grid is full" in str(exc.value)


def test_grid_returns_repr() -> None:
    """It returns expected repr."""
    grid = engine.Board()

    assert repr(grid) == f"Board({repr(grid.grid)})"


# ================ Test Player ================


def test_player_handles_mark() -> None:
    """It handles get and set for marks."""
    for player in (
        engine.HumanPlayer(PLAYER_A_NAME),
        engine.AIPlayer(PLAYER_B_NAME),
    ):
        assert player.get_mark() is None
        player.set_mark(MARK_X)
        assert player.get_mark() == MARK_X
        player.set_mark(MARK_O)
        assert player.get_mark() == MARK_O


@pytest.mark.xfail(reason="__repr__ to be updated")
def test_player_returns_repr() -> None:
    """It returns expected repr."""
    player_a = engine.HumanPlayer(PLAYER_A_NAME)
    player_b = engine.AIPlayer(PLAYER_B_NAME)

    assert repr(player_a) == f"HumanPlayer({repr(PLAYER_A_NAME)}, None)"
    player_a.set_mark(MARK_X)
    assert repr(player_a) == f"HumanPlayer({repr(PLAYER_A_NAME)}, {repr(MARK_X)})"

    assert repr(player_b) == f"AIPlayer({repr(PLAYER_B_NAME)}, None)"
    player_b.set_mark(MARK_O)
    assert repr(player_b) == f"AIPlayer({repr(PLAYER_B_NAME)}, {repr(MARK_O)})"


# ================ Test PlayersMatch ================


def test_players_match_inits() -> None:
    """It inits and returns expected attribute values."""
    player_a = engine.HumanPlayer(PLAYER_A_NAME)
    player_b = engine.AIPlayer(PLAYER_B_NAME)
    players_match = engine.PlayersMatch(player_a, player_b)
    assert bool(player_a in players_match.players) is True
    assert bool(player_b in players_match.players) is True
    assert players_match.current_player == player_a


def test_players_match_player_get_and_switch() -> None:
    """It handles current player get and switch."""
    player_a = engine.HumanPlayer(PLAYER_A_NAME)
    player_b = engine.AIPlayer(PLAYER_B_NAME)
    players_match = engine.PlayersMatch(player_a, player_b)
    assert players_match.current_player == player_a
    assert players_match.current() == player_a
    players_match.switch()
    assert players_match.current_player == player_b
    assert players_match.current() == player_b
    players_match.switch()
    assert players_match.current_player == player_a
    assert players_match.current() == player_a


def test_players_match_returns_repr() -> None:
    """It returns expected repr."""
    player_a = engine.HumanPlayer(PLAYER_A_NAME)
    player_b = engine.AIPlayer(PLAYER_B_NAME)
    players_match = engine.PlayersMatch(player_a, player_b)

    assert repr(players_match) == (
        f"PlayersMatch(({repr(player_a)}, {repr(player_b)}), {repr(player_a)})"
    )
