"""Implementation of the negamax algorithm for Tic Tac Toe Game."""
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from easyAI import AI_Player
from easyAI import Human_Player
from easyAI import Negamax
from easyAI import TwoPlayerGame

from tic_tac_toe_game.typing import Grid


class TicTacToe(TwoPlayerGame):  # type: ignore[misc]
    """TicTacToe class.

    The board positions are numbered as follows:
    1 2 3
    4 5 6
    7 8 9
    """

    def __init__(
        self,
        players: List[Union[AI_Player, Human_Player]],
        board: Optional[List[int]] = None,
        current_player: int = 1,
    ) -> None:
        """Inits."""
        self.players = players
        if board is None:
            board = [0 for _ in range(9)]
        self.board = board
        self.current_player = current_player  # player 1 starts.

    def possible_moves(self) -> List[int]:
        """Returns possible moves."""
        return [i + 1 for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move: Union[int, str]) -> None:
        """Make move."""
        self.board[int(move) - 1] = self.current_player

    def unmake_move(self, move: Union[int, str]) -> None:
        """Unmake move.

        Optional method (speeds up the AI)
        """
        self.board[int(move) - 1] = 0

    WIN_LINES = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],  # horiz.
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],  # vertical
        [1, 5, 9],
        [3, 5, 7],  # diagonal
    ]

    def lose(self, who: Optional[int] = None) -> bool:
        """Has the opponent "three in line?"."""
        if who is None:
            who = self.opponent_index
        wins = [
            all([(self.board[c - 1] == who) for c in line]) for line in self.WIN_LINES
        ]
        return any(wins)

    def is_over(self) -> bool:
        """Returns boolean indicating if the game is over."""
        return (
            (self.possible_moves() == [])
            or self.lose()
            or self.lose(who=self.current_player)
        )

    def show(self) -> None:
        """Prints the board."""
        print(
            "\n"
            + "\n".join(
                [
                    " ".join([[".", "O", "X"][self.board[3 * j + i]] for i in range(3)])
                    for j in range(3)
                ]
            )
        )

    def spot_string(self, i: int, j: int) -> str:
        """Returns sign associated to the cell state."""
        return ["_", "O", "X"][self.board[3 * j + i]]

    def scoring(self) -> int:
        """Returns scoring."""
        opp_won = self.lose()
        i_won = self.lose(who=self.current_player)
        if opp_won and not i_won:
            return -100
        if i_won and not opp_won:
            return 100
        return 0

    def winner(self) -> str:
        """Returns winner or tie status."""
        if self.lose(who=2):
            return "AI Wins"
        return "Tie"


GRID_CORRESPONDENCE = {
    1: (0, 0),
    2: (0, 1),
    3: (0, 2),
    4: (1, 0),
    5: (1, 1),
    6: (1, 2),
    7: (2, 0),
    8: (2, 1),
    9: (2, 2),
}


def from_negamax_grid_format(grid: List[int]) -> Grid:
    """Loads grid from a list of int."""
    # return [[elem if elem != 2 else -1 for elem in row] for row in grid]
    return [
        [elem if elem != 2 else -1 for elem in grid[i : i + 3]]
        for i in range(0, len(grid), 3)
    ]


def to_negamax_grid_format(grid: Grid) -> List[int]:
    """Dumps grid to list of int."""
    return [elem if elem != -1 else 2 for row in grid for elem in row]


def negamax_move(grid: Grid, mark: int) -> Tuple[int, int]:
    """Computes best move."""
    board = to_negamax_grid_format(grid)
    current_player = mark if mark != -1 else 2

    ttt = TicTacToe([Human_Player(), AI_Player(Negamax(6))], board, current_player)

    ai_move = ttt.get_move()
    chosen_cell = GRID_CORRESPONDENCE[ai_move]
    return chosen_cell
