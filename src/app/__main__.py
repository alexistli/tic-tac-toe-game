"""Command-line interface."""
import click
import eventlet

from app import create_app
from app import socketio

eventlet.monkey_patch()


@click.command()
@click.version_option()
def main() -> None:
    """Tic Tac Toe Game."""
    app = create_app()
    socketio.run(app)


if __name__ == "__main__":
    main(prog_name="game")  # pragma: no cover
