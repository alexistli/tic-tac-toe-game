"""Test cases for the game module."""
import random
from typing import List

import pytest

from tic_tac_toe_game import engine
from tic_tac_toe_game import errors

PLAYER_NAME = "Sapiens"
PLAYER_A_NAME = "U-Man"
PLAYER_B_NAME = "Botybot"

PLAYER_A = engine.HumanPlayer(1, PLAYER_A_NAME)
PLAYER_B = engine.AIPlayer(-1, PLAYER_B_NAME)

RANDOM_ROW = random.randint(0, 2)
RANDOM_COL = random.randint(0, 2)
RANDOM_COORD = (RANDOM_ROW, RANDOM_COL)

FULL_GRID_LOOSE = "1 -1 1 -1 -1 1 1 1 -1"

# X would win turns 7 and 9 if this grid si filled in the read direction.
WIN_X_MOVES = ((2, 0), (2, 2))
WIN_X_GRID = "1 -1 1 -1 1 -1 1 -1 1"

# O would win turns 7 and 9 if this grid si filled in the read direction.
WIN_O_MOVES = ((2, 2),)
WIN_O_GRID = "-1 1 1 1 -1 1 -1 1 -1"


def load_grid_from_string(grid_str: str) -> List[List[int]]:
    """Returns a grid by loading a grid passed as a string."""
    array = [int(cell) for cell in grid_str.split()]
    grid = [[int(cell) for cell in array[i : i + 3]] for i in range(0, len(array), 3)]
    return grid


# ================ Test Grid ================


def test_grid_init_succeeds() -> None:
    """It returns an empty grid."""
    empty_grid = [[engine.Board._empty_cell] * 3] * 3
    board = engine.Board()
    assert board.grid == empty_grid


def test_grid_frame_succeeds() -> None:
    """It returns a framed grid."""
    data_row_str = engine.Board._vertical_separator.join(["_"] * 3)
    separator_row_str = engine.Board._intersection.join(
        [engine.Board._horizontal_separator] * 3
    )
    framed_grid = ("\n" + separator_row_str + "\n").join([data_row_str] * 3)

    board = engine.Board()
    assert board.framed_grid() == framed_grid


def test_grid_handles_cell_operations() -> None:
    """It handles cell operations."""
    board = engine.Board()
    for row_index, row in enumerate(board.grid):
        for col_index, _cell in enumerate(row):
            coord = (row_index, col_index)
            assert board.is_empty_cell(coord) is True
            board.set_cell(coord, 1)
            assert board.get_cell(coord) == 1
            assert board.is_empty_cell(coord) is False


def test_grid_handles_cell_override() -> None:
    """It handles cell overriding attempt."""
    board = engine.Board()
    assert board.is_empty_cell(RANDOM_COORD) is True
    board.set_cell(RANDOM_COORD, 1)
    assert board.get_cell(RANDOM_COORD) == 1
    with pytest.raises(errors.OverwriteCellError):
        board.set_cell(RANDOM_COORD, -1)
        assert board.get_cell(RANDOM_COORD) == 1


def test_not_full_grid_returns_is_not_full() -> None:
    """It returns False when grid is not full."""
    # grid is empty
    board = engine.Board()
    assert board.is_full() is False

    # grid is neither empty nor full
    for mark in (1, -1):
        board = engine.Board()
        for row_index, row in enumerate(board.grid):
            for col_index, _cell in enumerate(row):
                assert board.is_full() is False
                board.set_cell((row_index, col_index), mark)


def test_full_grid_returns_is_full() -> None:
    """It returns True when grid is full."""
    board = engine.Board(load_grid_from_string(FULL_GRID_LOOSE))
    assert board.is_full() is True

    for mark in (1, -1):
        board = engine.Board()
        for row_index, row in enumerate(board.grid):
            for col_index, _cell in enumerate(row):
                board.set_cell((row_index, col_index), mark)
        assert board.is_full() is True


def test_not_is_winning_move() -> None:
    """It returns False if move is not a winning move."""
    loose_board = engine.Board(load_grid_from_string(FULL_GRID_LOOSE))
    board = engine.Board()
    # Transfers all cells from loosing_grid to the new grid.
    # Every move should be a loosing move.
    for row_index, row in enumerate(board.grid):
        for col_index, _cell in enumerate(row):
            coord = (row_index, col_index)
            mark = loose_board.get_cell(coord)
            board.set_cell(coord, mark)
            assert board.is_winning_move(coord, mark) is False


def test_is_winning_move() -> None:
    """It returns True if move is a winning move."""
    for win_grid, win_moves in ((WIN_X_GRID, WIN_X_MOVES), (WIN_O_GRID, WIN_O_MOVES)):
        model_board = engine.Board(load_grid_from_string(win_grid))
        board = engine.Board()
        # Transfers all cells from loosing_grid to the new grid.
        # Every move should be a loosing move.
        for row_index, row in enumerate(board.grid):
            for col_index, _cell in enumerate(row):
                coord = (row_index, col_index)
                mark = model_board.get_cell(coord)
                board.set_cell(coord, mark)
                is_winning = coord in win_moves
                assert bool(board.is_winning_move(coord, mark)) == is_winning


@pytest.mark.xfail(reason="random_available_cell method was moved")
def test_returns_random_available_cell_succeeds() -> None:
    """It returns a random available cell."""
    board = engine.Board()
    for _ in range(0, 9):
        # value = random.choice((1, -1))
        # cell = board.random_available_cell()
        # assert board.is_empty_cell(cell) is True
        # board.set_cell(cell, value)
        pass  # TODO: should fix this test
    assert board.is_full() is True


@pytest.mark.xfail(reason="random_available_cell method was moved")
def test_handles_random_available_cell_exception() -> None:
    """It raises `IndexError` if grid is full."""
    # grid = load_grid(FULL_GRID_LOOSE)  # TODO: should fix this test
    with pytest.raises(IndexError) as exc:
        # grid.random_available_cell()
        pass
    assert "Grid is full" in str(exc.value)


def test_grid_returns_repr() -> None:
    """It returns expected repr."""
    board = engine.Board()

    assert repr(board) == f"Board({repr(board.grid)})"


# ================ Test Player ================


def test_player_handles_mark() -> None:
    """It handles get and set for marks."""
    for player in (
        engine.HumanPlayer(1, PLAYER_A_NAME),
        engine.AIPlayer(1, PLAYER_B_NAME),
    ):
        assert player.get_mark() == 1
        player.set_mark(-1)
        assert player.get_mark() == -1
        player.set_mark(1)
        assert player.get_mark() == 1


def test_player_returns_repr() -> None:
    """It returns expected repr."""
    player_a = engine.HumanPlayer(1, PLAYER_A_NAME)
    player_b = engine.AIPlayer(-1, PLAYER_B_NAME)

    assert repr(player_a) == f"HumanPlayer({repr(PLAYER_A_NAME)}, {repr(1)}, None)"
    player_a.set_mark(-1)
    assert repr(player_a) == f"HumanPlayer({repr(PLAYER_A_NAME)}, {repr(-1)}, None)"

    assert (
        repr(player_b) == f"AIPlayer({repr(PLAYER_B_NAME)}, {repr(-1)}, 'naive_move')"
    )
    player_b.set_mark(1)
    assert repr(player_b) == f"AIPlayer({repr(PLAYER_B_NAME)}, {repr(1)}, 'naive_move')"


# ================ Test PlayersMatch ================


def test_players_match_inits() -> None:
    """It inits and returns expected attribute values."""
    player_a = engine.HumanPlayer(1, PLAYER_A_NAME)
    player_b = engine.AIPlayer(-1, PLAYER_B_NAME)
    players_match = engine.PlayersMatch(player_a, player_b)
    assert bool(player_a in players_match.players) is True
    assert bool(player_b in players_match.players) is True
    assert players_match.current_player == player_a


def test_players_match_player_get_and_switch() -> None:
    """It handles current player get and switch."""
    player_a = engine.HumanPlayer(1, PLAYER_A_NAME)
    player_b = engine.AIPlayer(-1, PLAYER_B_NAME)
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
    player_a = engine.HumanPlayer(1, PLAYER_A_NAME)
    player_b = engine.AIPlayer(-1, PLAYER_B_NAME)
    players_match = engine.PlayersMatch(player_a, player_b)

    assert repr(players_match) == (
        f"PlayersMatch(({repr(player_a)}, {repr(player_b)}), {repr(player_a)})"
    )
