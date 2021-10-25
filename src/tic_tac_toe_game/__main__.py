"""Command-line interface."""
import click

from tic_tac_toe_game.game import Game, Player, HumanPlayer, AIPlayer, Grid


@click.command()
@click.version_option()
def main() -> None:
    """Tic Tac Toe Game."""

    click.secho("hello", fg="green")
    if click.confirm("Do you want to play a game?", abort=True):
        click.echo("Let's play a game...")

    # init players
    human_player = HumanPlayer(name="Alexis")
    ai_player = AIPlayer()

    mark = click.prompt('Please pick a mark', type=click.Choice(["X", "O"], case_sensitive=False), default="X")
    click.echo(mark)

    game = Game(human_player, ai_player)

    # set marks
    if mark == "X":
        game.x_player = human_player
        game.o_player = ai_player
    else:
        game.x_player = ai_player
        game.o_player = human_player

    finished = False
    while not finished:
        # game.play_turn()
        next_player = game.get_next_player()
        game.grid.display()
        played_cell = click.prompt('Please pick a cell', type=click.Choice(["X", "O"], case_sensitive=False), default="X")
        game.grid.mark_cell(cell=played_cell, player=player)
        game.grid.display()
        finished = game.current_player.has_won() or game.grid.is_full()

    if game.current_player.has_won():
        print(f"Player {game.current_player} won!")
    elif game.grid.is_full():
        print("Player tied!")


if __name__ == "__main__":
    main(prog_name="tic-tac-toe-game")  # pragma: no cover
