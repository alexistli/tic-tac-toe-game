"""Implementation of the MCTS algorithm for Tic Tac Toe Game."""
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np
import numpy.typing as npt
from mctspy.games.common import TwoPlayersAbstractGameState
from mctspy.tree.nodes import TwoPlayersGameMonteCarloTreeSearchNode
from mctspy.tree.search import MonteCarloTreeSearch

from tic_tac_toe_game.typing import Grid


class Move:
    """Move class."""

    def __init__(self, x_coordinate: int, y_coordinate: int, value: float) -> None:
        """Inits."""
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value

    def __repr__(self) -> str:
        """Repr."""
        return f"x:{self.x_coordinate} y:{self.y_coordinate} v:{self.value}"


class TicTacToeGameState(TwoPlayersAbstractGameState):  # type: ignore[misc]
    """TicTacToeGameState class."""

    x = 1
    o = -1

    def __init__(self, state: npt.NDArray[np.float64], next_to_move: float = 1) -> None:
        """Inits."""
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Only 2D square boards allowed")
        self.board = state
        self.board_size: int = state.shape[0]
        self.next_to_move = next_to_move

    @property
    def game_result(self) -> Optional[float]:
        """Returns game result.

        This property should return:
         1 if player #1 wins
        -1 if player #2 wins
         0 if there is a draw
         None if result is unknown
        Returns
        -------
        int
        """
        # check if game is over
        rowsum = np.sum(self.board, 0)
        colsum = np.sum(self.board, 1)
        diag_sum_tl = self.board.trace()
        diag_sum_tr = self.board[::-1].trace()

        player_one_wins = any(rowsum == self.board_size)
        # uses fact that python booleans are considered numeric type
        player_one_wins += any(colsum == self.board_size)  # type: ignore[assignment]
        player_one_wins += diag_sum_tl == self.board_size
        player_one_wins += diag_sum_tr == self.board_size

        if player_one_wins:
            return self.x

        player_two_wins = any(rowsum == -self.board_size)
        # uses fact that python booleans are considered numeric type
        player_two_wins += any(colsum == -self.board_size)  # type: ignore[assignment]
        player_two_wins += diag_sum_tl == -self.board_size
        player_two_wins += diag_sum_tr == -self.board_size

        if player_two_wins:
            return self.o

        if np.all(self.board != 0):
            return 0.0

        # if not over - no result
        return None

    def is_game_over(self) -> bool:
        """Returns boolean indicating if the game is over.

        Simplest implementation may just be
        `return self.game_result() is not None`
        Returns
        -------
        boolean
        """
        return self.game_result is not None

    def is_move_legal(self, move: Move) -> bool:
        """Checks if move is legal."""
        # check if correct player moves
        if move.value != self.next_to_move:
            return False

        # check if inside the board on x-axis
        x_in_range = 0 <= move.x_coordinate < self.board_size
        if not x_in_range:
            return False

        # check if inside the board on y-axis
        y_in_range = 0 <= move.y_coordinate < self.board_size
        if not y_in_range:
            return False

        # finally check if board field not occupied yet
        return bool(self.board[move.x_coordinate, move.y_coordinate] == 0)

    def move(self, move: Move) -> "TicTacToeGameState":
        """Consumes action and returns resulting TwoPlayersAbstractGameState.

        Returns
        -------
        TwoPlayersAbstractGameState
        """
        if not self.is_move_legal(move):
            raise ValueError(f"move {move} on board {self.board} is not legal")
        new_board = np.copy(self.board)
        new_board[move.x_coordinate, move.y_coordinate] = move.value
        if self.next_to_move == TicTacToeGameState.x:
            next_to_move = TicTacToeGameState.o
        else:
            next_to_move = TicTacToeGameState.x

        return TicTacToeGameState(new_board, next_to_move)

    def get_legal_actions(self) -> List[Move]:
        """Returns list of legal action at current game state.

        Returns
        -------
        list of AbstractGameAction
        """
        indices = np.where(self.board == 0)
        return [
            Move(coords[0], coords[1], self.next_to_move)
            for coords in list(zip(indices[0], indices[1], strict=True))
        ]


def from_mcts_grid_format(grid: List[List[float]]) -> Grid:
    """Loads grid from a list of int."""
    return [[int(elem) for elem in row] for row in grid]


def to_mcts_grid_format(grid: Grid) -> List[List[float]]:
    """Dumps grid to list of int."""
    return [[float(elem) for elem in row] for row in grid]


def mcts_move(grid: Grid, mark: int) -> Tuple[int, int]:
    """Computes best move."""
    board = to_mcts_grid_format(grid)
    current_player = float(mark)

    state = np.array(board)
    initial_board_state = TicTacToeGameState(state=state, next_to_move=current_player)
    root = TwoPlayersGameMonteCarloTreeSearchNode(state=initial_board_state)
    mcts = MonteCarloTreeSearch(root)
    best_node = mcts.best_action(10000)

    board_diff = best_node.state.board - best_node.parent.state.board

    x_coords, y_coords = np.where(board_diff == current_player)
    chosen_cell = (x_coords[0], y_coords[0])
    return chosen_cell
