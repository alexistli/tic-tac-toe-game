"""Command-line interface."""
import click

from app import create_app


@click.command()
@click.version_option()
def main() -> None:
    """Tic Tac Toe Game."""
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main(prog_name="flask-game")  # pragma: no cover
