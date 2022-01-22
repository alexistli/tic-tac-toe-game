"""Test cases for the state module."""
import pytest

from tic_tac_toe_game import engine
from tic_tac_toe_game import state

ROOM = "test"
GAME = engine.build_game()


@pytest.mark.skip
def test_state():
    """TODO."""
    state.set_state(ROOM, GAME)
    loaded_game = state.get_state(ROOM)
    assert loaded_game == GAME
