"""Command-line interface."""
import click

from app import create_app
from app import socketio


@click.command()
@click.version_option()
def main() -> None:
    """Tic Tac Toe Game."""
    # Start Game: Start

    app = create_app()

    socketio.run(app, log_output=True)  # pragma: no cover


if __name__ == "__main__":
    main(prog_name="tic-tac-toe-game")  # pragma: no cover
