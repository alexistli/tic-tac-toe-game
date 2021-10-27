"""Command-line interface."""
import click

from tic_tac_toe_game.game import AIPlayer
from tic_tac_toe_game.game import Game
from tic_tac_toe_game.game import HumanPlayer


@click.command()
@click.version_option()
def main() -> None:
    """Tic Tac Toe Game."""
    click.secho("hello", fg="green")
    if click.confirm("Do you want to play a game?", abort=True):
        click.echo("Let's play a game...")

    mark = click.prompt(
        "Please pick a mark",
        type=click.Choice(["X", "O"], case_sensitive=False),
        default="X",
    )
    click.echo(mark)

    # init players
    human_player = HumanPlayer(name="Alexis")
    ai_player = AIPlayer()

    # set marks
    if mark == "X":
        human_player.set_mark("X")
        ai_player.set_mark("O")
        game = Game(human_player, ai_player)
    else:
        ai_player.set_mark("X")
        human_player.set_mark("O")
        game = Game(ai_player, human_player)

    finished = False
    while not finished:
        # game.play_turn()
        player = game.get_player()

        print("\n\n")
        print(f"{player.name}, it is your turn!")
        print("Current grid: \n")
        print(f"{game.grid.framed_grid()}\n")

        if isinstance(player, HumanPlayer):
            played_cell = click.prompt(
                "Please pick a cell (x, y)", type=click.Tuple([int, int])
            )
        else:
            played_cell = game.grid.random_available_cell()

        game.grid.set_cell(
            coord=played_cell, value=player.get_mark()  # type: ignore[arg-type]
        )

        if game.grid.is_winning_move(
            played_cell, player.get_mark()  # type: ignore[arg-type]
        ):
            print(f"Player {player.name} won!")
            finished = True
        elif game.grid.is_full():
            print("Players tied!")
            finished = True
        else:
            game.switch_player()


if __name__ == "__main__":
    main(prog_name="tic-tac-toe-game")  # pragma: no cover
