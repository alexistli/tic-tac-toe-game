"""Tic Tac Toe Game.

Rules:
    The object of Tic Tac Toe is to get three in a row.
    You play on a three by three game board.
    The first player is known as X and the second is O.
    Players alternate placing Xs and Os on the game board,
    until either opponent has three in a row or all nine squares are filled.
    X always goes first, and in the event that no one has three in a row,
    the stalemate is called a cat game.

Version 1.0: Player vs Dumb AI
    Human Player decide if he wants to start or not.
    Then roles are switched for every game.
    Dumb AI will place a mark on a random slot.


Version 2.0: Dumb AI + score limit
    Player scores are memorized and displayed.
    Player A starts, player B choose score limit.

        # sets score limit
        choose_score_limit(player=ai_player)

        game = Game()
        game.score_limit = 123
        game.current_turn = "X"
"""
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import List
from typing import Optional
from typing import Tuple

from tic_tac_toe_game.errors import OverwriteCellError


class Move:
    """Move performed by a Player on the Grid."""

    def __init__(self, x_coordinate, y_coordinate, value):
        """Inits."""
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value

    def __repr__(self):
        """Repr."""
        return (
            f"{self.__class__.__name__}"
            f"(x_coordinate: {self.x_coordinate}, "
            f"y_coordinate: {self.y_coordinate}, "
            f"value: {self.value})"
        )


class Board:
    """Board class.

    Attributes:
        grid: A 3*3 matrix of string values.
    """

    _empty_cell = "_"
    _vertical_separator = "│"
    _horizontal_separator = "─"
    _intersection = "┼"

    def __init__(self) -> None:
        """Inits Grid with an empty grid."""
        self.grid: List[List[str]] = [[Board._empty_cell] * 3 for _ in range(3)]
        self.history: List[Optional[Tuple[str, Tuple[int, int]]]] = []

    def get_cell(self, coord: Tuple[int, int]) -> str:
        """Returns value for cell located at `coord`."""
        return self.grid[coord[0]][coord[1]]

    def set_cell(self, coord: Tuple[int, int], value: str) -> None:
        """Sets `value` for cell located at `coord` if cell is empty."""
        coord_x, coord_y = coord
        if not self.is_empty_cell(coord):
            raise OverwriteCellError(coord)
        self.grid[coord_x][coord_y] = value
        self.history.append((value, coord))

    def get_last_play(self) -> Tuple[str, Tuple[int, int]]:
        """Returns last played cell and associated mark or None."""
        return self.history[-1] if len(self.history) else (None, None)

    def is_empty_cell(self, coord: Tuple[int, int]) -> bool:
        """Checks if cell located at `coord` is empty."""
        return bool(self.get_cell(coord) == Board._empty_cell)

    def is_full(self) -> bool:
        """Checks if grid is full. Gris is full if there is no empty cell left."""
        return not any(
            self.is_empty_cell((row_id, col_id))
            for row_id, row in enumerate(self.grid)
            for col_id, col in enumerate(row)
        )

    def is_winning_move(self, coord: Tuple[int, int], value: str) -> bool:
        """Checks if playing `value` at `coord` leads to a win.

        Only checks the combinations containing the cell with the given coordinates.
        Checks the one row, the one column and eventually the two diagonals.
        """
        has_winning_row = all([col == value for col in self.grid[coord[0]]])
        has_winning_col = all([row[coord[1]] == value for row in self.grid])

        has_winning_diag = False
        if coord[0] == coord[1]:
            has_winning_diag = all(
                self.grid[row_id][row_id] == value
                for row_id, row in enumerate(self.grid)
            )
        if coord[0] + coord[1] == 2:
            has_winning_diag = has_winning_diag or all(
                self.grid[2 - row_id][row_id] == value
                for row_id, row in enumerate(self.grid)
            )
        return bool(has_winning_row or has_winning_col or has_winning_diag)

    def framed_grid(self) -> str:
        """Returns the grid with an additional frame to facilitate reading."""
        framed = []
        for idx, row in enumerate(self.grid):
            framed.append(Board._vertical_separator.join(row))
            if idx != len(self.grid) - 1:
                framed.append(Board._intersection.join(Board._horizontal_separator * 3))
        return "\n".join(framed)

    @staticmethod
    def load_from_int_array(list_grid: List[List[int]], mapping):
        """Loads grid from a list of int."""
        grid = Board()
        grid.grid = [[mapping[elem] for elem in row] for row in list_grid]
        return grid

    def dump_to_int_array(self, mapping):
        """Dumps grid to list of int."""
        grid = [[mapping[elem] for elem in row] for row in self.grid]
        return grid

    def __repr__(self) -> str:
        """Returns instance representation."""
        return f"{self.__class__.__name__}({self.grid!r})"


class Player(ABC):
    """Base Player class.

    Attributes:
        name: The name of the player.
        mark: The value of the mark currently used. Must be "X" or "O".
    """

    def __init__(
        self, name: str, mark: Optional[str] = None, moves: Optional[Callable] = None
    ) -> None:
        """Constructor.

        Args:
            name: str, name of the player.
            mark: str, player's mark.
            moves: callable, handles choice of moves.
        """
        self.name = name
        self.mark = mark
        self.moves = moves

    def set_mark(self, mark: str) -> None:
        """Sets the player's mark for this game.

        Args:
            mark: str, player's mark
        """
        self.mark = mark

    def get_mark(self) -> Optional[str]:
        """Returns the player's mark for this game.

        Returns:
            A string with the value of the mark or None.
        """
        return self.mark

    @abstractmethod
    def ask_move(self, board) -> Tuple[int, int]:
        """Asks the player what move he wants to play."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Returns instance representation."""
        return (
            f"{self.__class__.__name__}({self.name!r}, {self.mark!r}, {self.moves!r})"
        )


class AIPlayer(Player):
    """Player class for an AI-managed player."""

    def __init__(
        self,
        name: str = "Botybot",
        mark: Optional[str] = None,
        moves: Optional[Callable] = None,
    ) -> None:
        """Constructor.

        Args:
            name: str, name of the player.
            mark: str, player's mark.
            moves: callable, handles choice of moves.
        """
        super().__init__(name=name, mark=mark, moves=moves)

    def ask_move(self, board) -> Tuple[int, int]:
        """Asks the player what move he wants to play."""
        if self.moves is not None:
            return self.moves(board, self.get_mark())
        return None


class HumanPlayer(Player):
    """Player class for a Human-managed player."""

    def __init__(
        self,
        name: str = "Human",
        mark: Optional[str] = None,
        moves: Optional[Callable] = None,
    ) -> None:
        """Constructor.

        Args:
            name: str, name of the player.
            mark: str, player's mark.
            moves: callable, handles choice of moves.
        """
        super().__init__(name=name, mark=mark, moves=moves)

    def ask_move(self, board) -> Tuple[int, int]:
        """Asks the player what move he wants to play."""
        if self.moves is not None:
            return self.moves(board, self.get_mark())
        return None


class PlayersMatch:
    """Matches players together and manages turns.

    Attributes:
        players: tuple(Player, Player), Players playing against each other.
        current_player: Player, Holds the player currently playing.
    """

    def __init__(self, player_x: Player, player_o: Player, start: str = "X") -> None:
        """Constructor.

        Args:
            player_x: Player, Player with the "X" mark. Will begin game.
            player_o: Player, Player with the "Y" mark.
            start: str, Mark starting the game.
        """
        self.players = (player_x, player_o)

        # Holds the player currently playing. Rules dictate that "X" starts the game.
        self.current_player: Player = player_x if start == "X" else player_o

    def update_ai_algorithm(self, algorithm):
        """Updates the AI algorithm of the AIPlayer."""
        ai_player = next(
            player for player in self.players if isinstance(player, AIPlayer)
        )
        ai_player.moves = algorithm

    def switch(self) -> None:  # pragma: no cover
        """Updates `current_player` with the other player."""
        self.current_player = next(
            player for player in self.players if player != self.current_player
        )

    def current(self) -> Player:
        """Returns `current_player`."""
        return self.current_player

    def __repr__(self) -> str:
        """Returns instance representation."""
        return f"{self.__class__.__name__}({self.players!r}, {self.current_player!r})"


class Engine:
    """Engine.

    Attributes:
        board: Board, The current board being played.
    """

    def __init__(
        self, player_1_mark: str, player_2_type: str, board: Board = None
    ) -> None:
        """Returns a Game instance initialized with players params."""
        player_1 = HumanPlayer("Player 1")

        if player_2_type == "H":
            player_2 = HumanPlayer("Player 2")
        else:
            player_2 = AIPlayer()

        # set marks
        if player_1_mark == "X":
            player_1.set_mark("X")
            player_2.set_mark("O")
            self.players_match = PlayersMatch(player_1, player_2)
        else:
            player_1.set_mark("O")
            player_2.set_mark("X")
            self.players_match = PlayersMatch(player_2, player_1)

        # Initialize an empty grid.
        self.board = board

    def get_move(self) -> Tuple[int, int]:
        """Gets a move from the current player.

        If the player is an
        AI_Player, then this method will invoke the AI algorithm to choose the
        move. If the player is a Human_Player, then the interaction with the
        human is via the text terminal.
        """
        return self.players_match.current().ask_move(self.board)

    def start_game(self) -> None:
        """TODO."""

    def end_game(self) -> None:
        """TODO."""

    def start_turn(self) -> None:
        """TODO."""

    def end_turn(self) -> None:
        """TODO."""

    def play_turn(self) -> None:
        """TODO."""
