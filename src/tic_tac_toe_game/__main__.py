"""Command-line interface."""
import click
import numpy as np
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch

from tic_tac_toe_game import engine
from tic_tac_toe_game.engine import Grid
from tic_tac_toe_game.tictactoe import TicTacToeGameState


@click.command()
@click.version_option()
def main() -> None:
    """Tic Tac Toe Game."""
    # Start Game: Start
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

    finished = False

    # Start Game: End

    while not finished:

        # Start Turn: Start
        player = game.players_match.current()

        print("\n\n")
        print(f"{player.name}, it is your turn!")
        print("Current grid: \n")
        print(f"{game.grid.framed_grid()}\n")

        if isinstance(player, engine.HumanPlayer):
            played_cell = click.prompt(
                "Please pick a cell xy", type=click.Tuple([int, int])
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
            game.players_match.switch()


@click.command()
@click.version_option()
def main2() -> None:
    """Tic Tac Toe Game."""
    # Start Game: Start
    click.secho("hello", fg="green")
    if click.confirm("Do you want to play a game?", abort=True):
        click.echo("Let's play a game...")

    player_1_mark = click.prompt(
        "Player 1, please pick your mark",
        type=click.Choice(["X", "O"], case_sensitive=False),
        default="X",
    )

    player_2_type = "B"

    state = np.zeros((3, 3))
    initial_board_state = TicTacToeGameState(state=state, next_to_move=1)

    game = engine.Engine(player_1_mark, player_2_type)
    game.grid = Grid()

    finished = False

    # Start Game: End

    while not finished:
        player = game.players_match.current()

        print("\n\n")
        print(f"{player.name}, it is your turn!")
        print("Current grid: \n")
        print(f"{game.grid.framed_grid()}\n")

        is_player_human = player.get_mark() == player_1_mark
        if is_player_human:
            # Player's turn
            played_cell = click.prompt(
                "Please pick a cell xy", type=click.Tuple([int, int])
            )
        else:
            # AI's turn
            # played_cell = game.grid.random_available_cell()
            next_to_move = initial_board_state.__getattribute__(
                player.get_mark().lower()
            )

            state = np.array(game.grid.dump_to_int_array())
            initial_board_state = TicTacToeGameState(
                state=state, next_to_move=next_to_move
            )
            root = TwoPlayersGameMonteCarloTreeSearchNode(state=initial_board_state)
            mcts = MonteCarloTreeSearch(root)
            best_node = mcts.best_action(10000)

            print("\nSub:")
            sub = best_node.state.board - best_node.parent.state.board
            print(sub)

            x_coords, y_coords = np.where(sub == next_to_move)
            print(x_coords, y_coords)
            print(x_coords[0], y_coords[0])
            played_cell = (x_coords[0], y_coords[0])

        # Start Turn: Start
        # player = game.players_match.current()

        # print("\n\n")
        # print(f"{player.name}, it is your turn!")
        # print("Current grid: \n")
        # print(f"{game.grid.framed_grid()}\n")

        # if isinstance(player, engine.HumanPlayer):
        #     played_cell = click.prompt(
        #         "Please pick a cell xy", type=click.Tuple([int, int])
        #     )
        # else:
        #     played_cell = game.grid.random_available_cell()

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
            game.players_match.switch()


@click.command()
@click.version_option()
def mctspy() -> None:
    """MCTSPY."""
    state = np.zeros((3, 3))
    state[1, 1] = 1
    state[2, 0] = -1
    # state[1, 0] = 1
    # state[1, 2] = -1
    # state[2, 1] = 1
    # state[0, 1] = -1
    # state[0, 0] = 1
    # state[2, 2] = -1
    # state[0, 2] = 1

    initial_board_state = TicTacToeGameState(state=state, next_to_move=1)

    root = TwoPlayersGameMonteCarloTreeSearchNode(state=initial_board_state)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(10000)

    print(best_node)
    print(best_node.q)
    print(best_node.n)
    print(best_node.state.board)

    print("\nBest node:")
    print(best_node.__dict__)
    print("\nBest node state:")
    print(best_node.state.__dict__)
    print(best_node.state.board)
    print("\nBest node parent:")
    print(best_node.parent.state.__dict__)
    print(best_node.parent.state.board)

    print("\nSub:")
    sub = best_node.state.board - best_node.parent.state.board
    print(sub)

    print(np.where(sub == 1))
    x_coords, y_coords = np.where(sub == 1)
    print(x_coords[0], y_coords[0])

    mark = "X"

    print(initial_board_state.next_to_move)
    print(initial_board_state.__getattribute__(mark.lower()))

    game = engine.Engine("X", "B")
    game.grid = Grid()
    print(game.grid.grid)
    to_array = game.grid.dump_to_int_array()
    print(to_array)
    to_grid = Grid.load_from_int_array(to_array)
    print(to_grid)


if __name__ == "__main__":
    main(prog_name="tic-tac-toe-game")  # pragma: no cover
