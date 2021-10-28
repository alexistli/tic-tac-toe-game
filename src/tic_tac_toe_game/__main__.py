"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Tic Tac Toe Game."""


if __name__ == "__main__":
    main(prog_name="tic-tac-toe-game")  # pragma: no cover
