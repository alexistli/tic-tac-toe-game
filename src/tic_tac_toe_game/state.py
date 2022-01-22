"""Game state persistence."""
import json

from tic_tac_toe_game import engine

# GET STATE


def get_state(room: str) -> engine.Engine:
    """TODO."""
    with open(f"{room}.json") as json_file:
        data = json.load(json_file)
        game = engine.Engine.from_dict(data)
        return game


# SET STATE
def set_state(room: str, game: engine.Engine) -> None:
    """TODO."""
    with open(f"{room}.json", "a") as json_file:
        json.dump(game.to_dict(), json_file)
