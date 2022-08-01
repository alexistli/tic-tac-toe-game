"""Tic Tac Toe Game."""
import json
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Tuple
from typing import Union

from tic_tac_toe_game.AI.mcts import mcts_move
from tic_tac_toe_game.AI.naive import naive_move
from tic_tac_toe_game.AI.negamax import negamax_move
from tic_tac_toe_game.errors import OverwriteCellError
from tic_tac_toe_game.typing import Coordinates
from tic_tac_toe_game.typing import Grid


class Move:
    """Move performed by a Player on the Grid."""

    def __init__(
        self,
        x: Union[int, float, str],
        y: Union[int, float, str],
        player: Union[int, float, str],
    ) -> None:
        """Inits."""
        self.x = int(x)
        self.y = int(y)
        self._player = int(player)

    @property
    def player(self) -> int:
        """TODO."""
        return self._player

    @player.setter
    def player(self, value: Union[int, float, str]) -> None:
        if int(value) != 1 and int(value) != -1:
            raise ValueError("Player should be 1 or -1")
        self._player = int(value)

    @property
    def coordinates(self) -> Coordinates:
        """TODO."""
        return self.x, self.y

    def __repr__(self) -> str:
        """Repr."""
        return f"{self.__class__.__name__}({self.x!r}, {self.y!r}, {self.player!r})"

    def to_dict(self) -> Dict[str, Union[int, str]]:
        """Converts the Move instance to a dictionary."""
        return dict(
            x=self.x,
            y=self.y,
            player=self.player,
            __class=self.__class__.__name__,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Union[int, str]]) -> "Move":
        """Constructs Move instance from dictionary."""
        data = dict(data)  # local copy
        if not isinstance(data, dict) or data.pop("__class") != cls.__name__:
            raise ValueError
        return cls(**data)

    def __eq__(self, other: object) -> bool:
        """Check whether other equals self elementwise."""
        if not isinstance(other, Move):
            return False
        return self.__dict__ == other.__dict__


class Board:
    """Board class.

    Attributes:
        grid: A 3*3 matrix of string values.
    """

    x = 1
    o = -1
    _empty_cell = 0
    _vertical_separator = "│"
    _horizontal_separator = "─"
    _intersection = "┼"
    _marks = {0: "_", -1: "O", 1: "X"}

    def __init__(
        self,
        grid: Optional[Grid] = None,
        history: Optional[List[Move]] = None,
    ) -> None:
        """Inits Grid with an empty grid."""
        if grid is None:
            grid = [[Board._empty_cell] * 3 for _ in range(3)]
        self.grid: Grid = grid
        if history is None:
            history = []
        self.history: List[Move] = history

    def get_cell(self, coord: Coordinates) -> int:
        """Returns value for cell located at `coord`."""
        return self.grid[coord[0]][coord[1]]

    def make_move(self, move: Move) -> None:
        """Sets `value` for cell located at `coord` if cell is empty.

        Consumes action.
        """
        if not self.is_empty_cell(move.coordinates):
            raise OverwriteCellError(move.coordinates)
        self.grid[move.x][move.y] = move.player
        self.history.append(move)

    def is_empty_cell(self, coord: Coordinates) -> bool:
        """Checks if cell located at `coord` is empty."""
        return bool(self.get_cell(coord) == Board._empty_cell)

    def is_full(self) -> bool:
        """Checks if grid is full. Gris is full if there is no empty cell left."""
        return not any(
            self.is_empty_cell((row_id, col_id))
            for row_id, row in enumerate(self.grid)
            for col_id, col in enumerate(row)
        )

    def is_winning_move(self, move: Move) -> bool:
        """Checks if playing `value` at `coord` leads to a win.

        Only checks the combinations containing the cell with the given coordinates.
        Checks the one row, the one column and eventually the two diagonals.
        """
        has_winning_row = all([cell == move.player for cell in self.grid[move.x]])
        has_winning_col = all([row[move.y] == move.player for row in self.grid])

        has_winning_diag = False
        if move.x == move.y:
            has_winning_diag = all(
                self.grid[row_id][row_id] == move.player
                for row_id, row in enumerate(self.grid)
            )
        if move.x + move.y == 2:
            has_winning_diag = has_winning_diag or all(
                self.grid[2 - row_id][row_id] == move.player
                for row_id, row in enumerate(self.grid)
            )
        return bool(has_winning_row or has_winning_col or has_winning_diag)

    def display(self) -> List[List[str]]:
        """Returns the grid."""
        return [[Board._marks[elem] for elem in row] for row in self.grid]

    def framed_grid(self) -> str:
        """Returns the grid with an additional frame to facilitate reading."""
        framed = []
        for idx, row in enumerate(self.display()):
            framed.append(Board._vertical_separator.join(row))
            if idx != len(self.grid) - 1:
                framed.append(Board._intersection.join(Board._horizontal_separator * 3))
        return "\n".join(framed)

    def winner(self) -> Optional[int]:
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
        try:
            last_move = self.history[-1]
        except IndexError:  # no history means there is no winner
            return None

        has_winning_row = all(
            [cell == last_move.player for cell in self.grid[last_move.x]]
        )
        has_winning_col = all(
            [row[last_move.y] == last_move.player for row in self.grid]
        )

        has_winning_diag = False
        if last_move.x == last_move.y:
            has_winning_diag = all(
                self.grid[row_id][row_id] == last_move.player
                for row_id, row in enumerate(self.grid)
            )
        if last_move.x + last_move.y == 2:
            has_winning_diag = has_winning_diag or all(
                self.grid[2 - row_id][row_id] == last_move.player
                for row_id, row in enumerate(self.grid)
            )
        if has_winning_row or has_winning_col or has_winning_diag:
            return last_move.player
        elif self.is_full():
            return 0
        else:
            return None

    def is_over(self) -> bool:
        """Returns boolean indicating if the game is over.

        Simplest implementation may just be
        `return self.game_result() is not None`
        Returns
        -------
        boolean
        """
        return self.winner() is not None

    def is_tie(self) -> bool:
        """Returns boolean indicating if the game is over.

        Simplest implementation may just be
        `return self.game_result() is not None`
        Returns
        -------
        boolean
        """
        return self.winner() == 0

    def is_won(self) -> bool:
        """Returns boolean indicating if the game is over.

        Simplest implementation may just be
        `return self.game_result() is not None`
        Returns
        -------
        boolean
        """
        return self.is_over() and not self.is_tie()

    def to_json(self) -> str:
        """Creates a JSON representation of an instance of Board."""
        d = {"__class": self.__class__.__name__, **self.__dict__}
        return json.dumps(d, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, json_string: str) -> "Board":
        """Instantiate a Board object from a JSON description of it.

        The JSON should have been produced by calling .to_json() on the object.

        Args:
            json_string: str, A serialized JSON object.

        Returns:
            An instance of the Board class.

        Raises:
            ValueError: If json_string was not produced by calling .to_json().
        """
        attributes = json.loads(json_string)
        if (
            not isinstance(attributes, dict)
            or attributes.pop("__class") != cls.__name__
        ):
            raise ValueError
        return cls(**attributes)

    def __repr__(self) -> str:
        """Returns instance representation."""
        return f"{self.__class__.__name__}({self.grid!r}, {self.history!r})"

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Board instance to a dictionary."""
        return dict(
            grid=self.grid,
            history=[move.to_dict() for move in self.history],
            __class=self.__class__.__name__,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Board":
        """Constructs Board instance from dictionary."""
        data = dict(data)  # local copy
        if not isinstance(data, dict) or data.pop("__class") != cls.__name__:
            raise ValueError
        return cls(
            data.get("grid"),
            [Move.from_dict(move) for move in data.get("history")],
        )

    def __eq__(self, other: object) -> bool:
        """Check whether other equals self elementwise."""
        if not isinstance(other, Board):
            return False
        return self.__dict__ == other.__dict__


class Player(ABC):
    """Base Player class.

    Attributes:
        name: The name of the player.
        mark: The value of the mark currently used. Must be "X" or "O".
    """

    _available_moves = [naive_move, mcts_move, negamax_move]

    def __init__(
        self,
        mark: int,
        name: str,
        moves: Optional[Callable[[Grid, int], Coordinates]] = None,
        score: int = 0,
    ) -> None:
        """Constructor.

        Args:
            name: str, name of the player.
            mark: str, player's mark.
            moves: callable, handles choice of moves.
            score: int, player's score.
        """
        self.name = name
        self._mark = mark
        self.moves = moves
        self._score = score

    def set_mark(self, mark: int) -> None:
        """Sets the player's mark for this game.

        Args:
            mark: int, player's mark
        """
        self._mark = mark

    def get_mark(self) -> int:
        """Returns the player's mark for this game.

        Returns:
            An integer with the value of the mark.
        """
        return self._mark

    def display_mark(self) -> str:
        """Returns the pretty print mark for the player.

        Returns:
            A string with the value of the mark.
        """
        return "X" if self._mark == 1 else "O"

    def record_win(self) -> None:
        """Records player's win and updates score."""
        self._score += 1

    def get_score(self) -> int:
        """Returns the player's score for this game.

        Returns:
            An integer with the value of the score.
        """
        return self._score

    @abstractmethod
    def ask_move(self, grid: Grid) -> Optional[Coordinates]:
        """Asks the player what move he wants to play."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Returns instance representation."""
        repr_moves = (
            self.moves.__name__ if self.moves in self._available_moves else None
        )
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self._mark!r}, {repr_moves!r}, {self._score!r})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Player instance to a dictionary."""
        repr_moves = (
            self.moves.__name__ if self.moves in self._available_moves else None
        )
        return dict(
            name=self.name,
            mark=self._mark,
            moves=repr_moves,
            score=self._score,
            __class=self.__class__.__name__,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        """Constructs Player instance from dictionary."""
        if not isinstance(data, dict):
            raise ValueError
        data = dict(data)  # local copy
        class_name = data.pop("__class")
        available_moves = {move.__name__: move for move in cls._available_moves}
        data["moves"] = (
            available_moves[data["moves"]] if data["moves"] in available_moves else None
        )
        if class_name == "HumanPlayer":
            return HumanPlayer(**data)
        elif class_name == "AIPlayer":
            return AIPlayer(**data)
        raise ValueError("`class__` must be 'HumanPlayer' or 'AIPlayer'")

    def __eq__(self, other: object) -> bool:
        """Check whether other equals self elementwise."""
        if not isinstance(other, Player):
            return False
        return self.__dict__ == other.__dict__


class AIPlayer(Player):
    """Player class for an AI-managed player."""

    def __init__(
        self,
        mark: int,
        name: str,
        moves: Optional[Callable[[Grid, int], Coordinates]] = naive_move,
        score: int = 0,
    ) -> None:
        """Constructor.

        Args:
            name: str, name of the player.
            mark: str, player's mark.
            moves: callable, handles choice of moves.
            score: int, player's score.
        """
        super().__init__(mark=mark, name=name, moves=moves, score=score)

    def ask_move(self, grid: Grid) -> Optional[Coordinates]:
        """Asks the player what move he wants to play."""
        if self.moves is not None:
            return self.moves(grid, self.get_mark())
        return None


class HumanPlayer(Player):
    """Player class for a Human-managed player."""

    def __init__(
        self,
        mark: int,
        name: str,
        moves: Optional[Callable[[Grid, int], Coordinates]] = None,
        score: int = 0,
    ) -> None:
        """Constructor.

        Args:
            name: str, name of the player.
            mark: str, player's mark.
            moves: callable, handles choice of moves.
            score: int, player's score.
        """
        super().__init__(mark=mark, name=name, moves=moves, score=score)

    def ask_move(self, grid: Grid) -> Optional[Coordinates]:
        """Asks the player what move he wants to play."""
        if self.moves is not None:
            return self.moves(grid, self.get_mark())
        return None


class PlayersMatch:
    """Matches players together and manages turns.

    Attributes:
        players: tuple(Player, Player), Players playing against each other.
        _current_player: Player, Holds the player currently playing.
    """

    def __init__(self, player_x: Player, player_o: Player) -> None:
        """Constructor.

        Args:
            player_x: Player, Player with the "X" mark. Will begin game.
            player_o: Player, Player with the "Y" mark.
        """
        self.players: Tuple[Player, ...] = (player_x, player_o)

        # Holds the player currently playing. Rules dictate that "X" starts the game.
        self._current_player: Player = player_x

    def update_ai_algorithm(
        self, algorithm: Callable[[Grid, int], Coordinates]
    ) -> None:
        """Updates the AI algorithm of the AIPlayer."""
        ai_player = next(
            player for player in self.players if isinstance(player, AIPlayer)
        )
        ai_player.moves = algorithm

    def switch(self) -> None:  # pragma: no cover
        """Updates `_current_player` with the other player."""
        self._current_player = next(
            player for player in self.players if player != self._current_player
        )

    def current(self) -> Player:
        """Returns `_current_player`."""
        return self._current_player

    def player(self, id_: int) -> Player:
        """Returns `_current_player`."""
        if id_ != 1 and id_ != -1:
            raise ValueError("id argument should be 1 or -1")
        return next(player for player in self.players if player.get_mark() == id_)

    def __repr__(self) -> str:
        """Returns instance representation."""
        return f"{self.__class__.__name__}({self.players!r}, {self._current_player!r})"

    def to_dict(self) -> Dict[str, Any]:
        """Converts the PlayersMatch instance to a dictionary."""
        return dict(
            players=[player.to_dict() for player in self.players],
            current_player=self._current_player.to_dict(),
            __class=self.__class__.__name__,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlayersMatch":
        """Constructs PlayersMatch instance from dictionary."""
        data = dict(data)  # local copy
        players = [Player.from_dict(player) for player in data.get("players")]
        current_player = Player.from_dict(data.get("current_player"))
        players_match = cls(*players)
        if players_match.current() != current_player:
            players_match.switch()
        return players_match

    def __eq__(self, other: object) -> bool:
        """Check whether other equals self elementwise."""
        if not isinstance(other, PlayersMatch):
            return False
        return self.__dict__ == other.__dict__


class TicTacToeGame:
    """TicTacToeGame.

    Attributes:
        board: Board, The current board being played.
    """

    def __init__(self, players_match: PlayersMatch, board: Board) -> None:
        """Returns a Game instance initialized with players params."""
        self.players_match = players_match
        self.board = board

    def get_move(self) -> Optional[Coordinates]:
        """Gets a move from the current player.

        If the player is an
        AI_Player, then this method will invoke the AI algorithm to choose the
        move. If the player is a Human_Player, then the interaction with the
        human is via the text terminal.
        """
        return self.players_match.current().ask_move(self.board.grid)

    def get_scores(self) -> List[Tuple[str, int]]:
        """Returns the scores."""
        scores = [
            (player.display_mark(), player.get_score())
            for player in self.players_match.players
        ]
        return scores

    def winner(self) -> Optional[Player]:
        """TODO."""
        board_winner = self.board.winner()
        return (
            self.players_match.player(board_winner)
            if board_winner == 1 or board_winner == -1
            else None
        )

    def __repr__(self) -> str:
        """Returns instance representation."""
        return f"{self.__class__.__name__}({self.players_match!r}, {self.board!r})"

    def to_dict(self) -> Dict[str, Any]:
        """Converts the TicTacToeGame instance to a dictionary."""
        return dict(
            players_match=self.players_match.to_dict(),
            board=self.board.to_dict(),
            __class=self.__class__.__name__,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TicTacToeGame":
        """Constructs TicTacToeGame instance from dictionary."""
        return cls(
            PlayersMatch.from_dict(data.get("players_match")),
            Board.from_dict(data.get("board")),
        )

    def __eq__(self, other: object) -> bool:
        """Check whether other equals self elementwise."""
        if not isinstance(other, TicTacToeGame):
            return False
        return self.__dict__ == other.__dict__


MODE = Literal["single", "multi"]


def build_game(
    player_1_name: Optional[str] = None,
    player_2_name: Optional[str] = None,
    player_1_starts: bool = True,
    mode: MODE = "single",
) -> TicTacToeGame:
    """Returns a game object."""
    player_1_mark = 1 if player_1_starts is True else -1
    player_1: Player = HumanPlayer(player_1_mark, player_1_name or "Player 1")

    player_2_mark = 0 - player_1_mark
    player_2: Player
    if mode == "single":
        player_2 = AIPlayer(player_2_mark, player_2_name or "Bot")
    else:
        player_2 = HumanPlayer(player_2_mark, player_2_name or "Player 2")

    return TicTacToeGame(PlayersMatch(player_1, player_2), Board())
