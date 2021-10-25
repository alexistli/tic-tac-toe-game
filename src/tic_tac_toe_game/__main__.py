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

    # set marks
    if mark == "X":
        human_player.set_mark("X")
        ai_player.set_mark("O")
        x_player = human_player
        o_player = ai_player
    else:
        ai_player.set_mark("X")
        human_player.set_mark("O")
        x_player = ai_player
        o_player = human_player

    game = Game(x_player, o_player)

    finished = False
    while not finished:
        # game.play_turn()
        game.switch_player()
        player = game.get_player()
        print(game.grid.framed_grid())

        if player.kind == "Human":
            played_cell = click.prompt('Please pick a cell (x, y)', type=click.Tuple([int, int]))
        else:
            played_cell = player.choose_cell(game.grid)

        game.grid.set_cell(coord=played_cell, value=player.mark)

        if game.grid.is_winning_move(played_cell, player.mark):
            print(f"Player {player.name} won!")
            finished = True
        elif game.grid.is_full():
            print("Players tied!")
            finished = True


if __name__ == "__main__":
    main(prog_name="tic-tac-toe-game")  # pragma: no cover
