"""Command-line interface."""
import click

from tic_tac_toe_game import engine
from tic_tac_toe_game.engine import Board


@click.command()
@click.version_option()
def main() -> None:
    """Tic Tac Toe Game."""
    click.secho("hello", fg="green")
    if click.confirm("Do you want to play a game?", abort=True):
        click.echo("Let's play a game...")

    player_1_mark = click.prompt(
        "Player 1, please pick your mark",
        type=click.Choice(["X", "O"], case_sensitive=False),
        default="X",
    )

    player_2_type = click.prompt(
        "Player 2, are you Human (H) or a Bot (B)?",
        type=click.Choice(["H", "B"], case_sensitive=False),
        default="B",
    )

    game = engine.Engine(player_1_mark, player_2_type)
    game.board = Board()

    finished = False

    while not finished:
        player = game.players_match.current()

        print("\n\n")
        print(f"{player.name}, it is your turn!")
        print("Current grid: \n")
        print(f"{game.board.framed_grid()}\n")

        if isinstance(player, engine.HumanPlayer):
            played_cell = click.prompt(
                "Please pick a cell xy", type=click.Tuple([int, int])
            )
        else:
            # TODO: Upgrade with any possible strategy
            played_cell = game.board.random_available_cell()

        game.board.set_cell(
            coord=played_cell, value=player.get_mark()  # type: ignore[arg-type]
        )

        if game.board.is_winning_move(
            played_cell, player.get_mark()  # type: ignore[arg-type]
        ):
            print(f"Player {player.name} won!")
            finished = True
        elif game.board.is_full():
            print("Players tied!")
            finished = True
        else:
            game.players_match.switch()


if __name__ == "__main__":
    main(prog_name="tic-tac-toe-game")  # pragma: no cover
