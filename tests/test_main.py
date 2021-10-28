"""Test cases for the __main__ module."""
import pytest
from click.testing import CliRunner

from tic_tac_toe_game import __main__
from tic_tac_toe_game import engine


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


# ================ Test CLI ================


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(__main__.main)
    assert result.exit_code == 1


# ================ Test CLI ================


def test_game_init_returns_game() -> None:
    """It returns an object of type Game."""
    player_a_mark = "X"
    player_b_type = "H"
    game = __main__.game_init(player_a_mark, player_b_type)
    assert isinstance(game, engine.Game)
