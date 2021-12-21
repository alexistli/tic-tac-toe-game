"""Implementation of the negamax algorithm for Tic Tac Toe Game."""
from easyAI import AI_Player
from easyAI import Human_Player
from easyAI import Negamax
from easyAI import TwoPlayerGame


class TicTacToe(TwoPlayerGame):
    """TicTacToe class.

    The board positions are numbered as follows:
    1 2 3
    4 5 6
    7 8 9
    """

    def __init__(self, players):
        """Inits."""
        self.players = players
        self.board = [0 for i in range(9)]
        self.current_player = 1  # player 1 starts.

    def load_board(self, array_board):
        """Loads board from 2D array."""
        board = [element for row in array_board for element in row]
        self.board = board

    def possible_moves(self):
        """Returns possible moves."""
        return [i + 1 for i, e in enumerate(self.board) if e == 0]

    def make_move(self, move):
        """Make move."""
        self.board[int(move) - 1] = self.current_player

    def unmake_move(self, move):
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

    def lose(self, who=None):
        """Has the opponent "three in line?"."""
        if who is None:
            who = self.opponent_index
        wins = [
            all([(self.board[c - 1] == who) for c in line]) for line in self.WIN_LINES
        ]
        return any(wins)

    def is_over(self):
        """Returns boolean indicating if the game is over."""
        return (
            (self.possible_moves() == [])
            or self.lose()
            or self.lose(who=self.current_player)
        )

    def show(self):
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

    def spot_string(self, i, j):
        """Returns sign associated to the cell state."""
        return ["_", "O", "X"][self.board[3 * j + i]]

    def scoring(self):
        """Returns scoring."""
        opp_won = self.lose()
        i_won = self.lose(who=self.current_player)
        if opp_won and not i_won:
            return -100
        if i_won and not opp_won:
            return 100
        return 0

    def winner(self):
        """Returns winner or tie status."""
        if self.lose(who=2):
            return "AI Wins"
        return "Tie"


FROM_MARK = {"X": 1, "O": 2, "_": 0}
TO_MARK = {0: "_", 1: "X", 2: "O"}

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


def negamax_best_move(board, mark):
    """Computes best move."""
    list_grid = board.dump_to_int_array(FROM_MARK)
    player = FROM_MARK[mark]

    ttt = TicTacToe([Human_Player(), AI_Player(Negamax(6))])
    ttt.load_board(list_grid)
    ttt.current_player = player

    ai_move = ttt.get_move()
    chosen_cell = GRID_CORRESPONDENCE[ai_move]
    return chosen_cell
