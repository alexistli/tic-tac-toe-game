"""Game state persistence."""
import json
from pathlib import Path

from tic_tac_toe_game import engine


basedir = Path(__file__).resolve().parent


# GET STATE
def get_state(room: str) -> engine.TicTacToeGame:
    """TODO."""
    with open(Path(basedir).joinpath(f"{room}.json")) as json_file:
        data = json.load(json_file)
    game = engine.TicTacToeGame.from_dict(data)
    return game


# SET STATE
def set_state(room: str, game: engine.TicTacToeGame) -> None:
    """TODO."""
    with open(Path(basedir).joinpath(f"{room}.json"), "w") as json_file:
        json.dump(game.to_dict(), json_file, indent=4, sort_keys=True)
    return
