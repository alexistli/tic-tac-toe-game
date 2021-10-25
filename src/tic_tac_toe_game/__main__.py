"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Tic Tac Toe Game."""

    click.secho("hello", fg="green")
    if click.confirm("Do you want to play a game?", abort=True):
        click.echo("Let's play a game...")

    value = click.prompt('Please pick a player', type=click.Choice(["A", "B"], case_sensitive=False), default="A")
    click.echo(value)


if __name__ == "__main__":
    main(prog_name="tic-tac-toe-game")  # pragma: no cover
