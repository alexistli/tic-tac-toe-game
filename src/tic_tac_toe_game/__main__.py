"""Command-line interface."""
import click

from tic_tac_toe_game import engine


@click.command()
@click.version_option()
def main() -> None:
    """Tic Tac Toe Game."""
    click.secho("hello", fg="green")
    if click.confirm("Do you want to play a game?", abort=True):
        click.echo("Let's play a game...")

    player_a_mark = click.prompt(
        "Please pick a mark",
        type=click.Choice(["X", "O"], case_sensitive=False),
        default="X",
    )
    click.echo(player_a_mark)

    player_b_type = click.prompt(
        "Second player human or bot?",
        type=click.Choice(["H", "B"], case_sensitive=False),
        default="B",
    )
    click.echo(player_b_type)

    game = game_init(player_a_mark, player_b_type)

    finished = False
    while not finished:
        player = game.current()

        print("\n\n")
        print(f"{player.name}, it is your turn!")
        print("Current grid: \n")
        print(f"{game.grid.framed_grid()}\n")

        if isinstance(player, engine.HumanPlayer):
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
            game.switch()


def game_init(player_a_mark: str, player_b_type: str) -> engine.PlayersMatch:
    """Returns a Game instance initialized with players params."""
    # init players
    player_a: engine.Player
    player_b: engine.Player

    if player_b_type == "H":
        player_a = engine.HumanPlayer("Human 1")
        player_b = engine.HumanPlayer("Human 2")
    else:
        player_a = engine.HumanPlayer()
        player_b = engine.AIPlayer()
    # set marks
    if player_a_mark == "X":
        player_a.set_mark("X")
        player_b.set_mark("O")
        game = engine.PlayersMatch(player_a, player_b)
    else:
        player_b.set_mark("X")
        player_a.set_mark("O")
        game = engine.PlayersMatch(player_b, player_a)
    return game


if __name__ == "__main__":
    main(prog_name="tic-tac-toe-game")  # pragma: no cover
