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
import ast
import json
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Sequence
from typing import Tuple

from tic_tac_toe_game.AI.mcts import mcts_move
from tic_tac_toe_game.AI.naive import naive_move
from tic_tac_toe_game.AI.negamax import negamax_move
from tic_tac_toe_game.errors import OverwriteCellError


class Move:
    """Move performed by a Player on the Grid."""

    def __init__(self, x_coordinate: int, y_coordinate: int, value: str) -> None:
        """Inits."""
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value

    def __repr__(self) -> str:
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

    x = 1
    y = -1
    _empty_cell = 0
    _vertical_separator = "│"
    _horizontal_separator = "─"
    _intersection = "┼"
    _marks = {0: "_", -1: "O", 1: "X"}

    def __init__(self, grid: Optional[List[List[int]]] = None) -> None:
        """Inits Grid with an empty grid."""
        if grid is None:
            grid = [[Board._empty_cell] * 3 for _ in range(3)]
        self.grid: List[List[int]] = grid

    def get_cell(self, coord: Sequence[int]) -> int:
        """Returns value for cell located at `coord`."""
        return self.grid[coord[0]][coord[1]]

    def set_cell(self, coord: Sequence[int], value: int) -> None:
        """Sets `value` for cell located at `coord` if cell is empty."""
        coord_x, coord_y = coord
        if not self.is_empty_cell(coord):
            raise OverwriteCellError(coord)
        self.grid[coord_x][coord_y] = value

    def is_empty_cell(self, coord: Sequence[int]) -> bool:
        """Checks if cell located at `coord` is empty."""
        return bool(self.get_cell(coord) == Board._empty_cell)

    def is_full(self) -> bool:
        """Checks if grid is full. Gris is full if there is no empty cell left."""
        return not any(
            self.is_empty_cell((row_id, col_id))
            for row_id, row in enumerate(self.grid)
            for col_id, col in enumerate(row)
        )

    def is_winning_move(self, coord: Tuple[int, int], value: int) -> bool:
        """Checks if playing `value` at `coord` leads to a win.

        Only checks the combinations containing the cell with the given coordinates.
        Checks the one row, the one column and eventually the two diagonals.
        """
        has_winning_row = all([cell == value for cell in self.grid[coord[0]]])
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
        return f"{self.__class__.__name__}({self.grid!r})"

    def to_dict(self) -> Dict[str, Any]:
        """Converts the PlayersMatch instance to a dictionary."""
        return {"__class": self.__class__.__name__, **self.__dict__}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Board":
        """Constructs Board instance from dictionary."""
        if not isinstance(data, dict) or data.pop("__class") != cls.__name__:
            raise ValueError
        return cls(**data)

    def __eq__(self, other: "Board"):
        """Check whether other equals self elementwise."""
        if not isinstance(other, Board):
            return False
        attr_keys = self.__dict__.keys()
        return all(
            self.__getattribute__(key) == other.__getattribute__(key)
            for key in attr_keys
        )


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
        moves: Optional[Callable[[List[List[int]], int], Tuple[int, int]]] = None,
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
        self.mark = mark
        self.moves = moves
        self.score = score

    def set_mark(self, mark: int) -> None:
        """Sets the player's mark for this game.

        Args:
            mark: int, player's mark
        """
        self.mark = mark

    def get_mark(self) -> int:
        """Returns the player's mark for this game.

        Returns:
            An integer with the value of the mark.
        """
        return self.mark

    def display_mark(self) -> str:
        """Returns the pretty print mark for the player.

        Returns:
            A string with the value of the mark.
        """
        return "X" if self.mark == 1 else "O"

    def record_win(self) -> None:
        """Records player's win and updates score."""
        self.score += 1

    def get_score(self) -> int:
        """Returns the player's score for this game.

        Returns:
            An integer with the value of the score.
        """
        return self.score

    @abstractmethod
    def ask_move(self, grid: List[List[int]]) -> Optional[Tuple[int, int]]:
        """Asks the player what move he wants to play."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Returns instance representation."""
        repr_moves = (
            self.moves.__name__ if self.moves in self._available_moves else None
        )
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.mark!r}, {repr_moves!r}, {self.score!r})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Player instance to a dictionary."""
        repr_moves = (
            self.moves.__name__ if self.moves in self._available_moves else None
        )
        return dict(
            name=self.name,
            mark=self.mark,
            moves=repr_moves,
            score=self.score,
            __class=self.__class__.__name__,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Player":
        """Constructs Player instance from dictionary."""
        data = dict(data)  # local copy
        class_name = data.pop("__class")
        available_moves = [move.__name__ for move in cls._available_moves]
        data["moves"] = (
            ast.literal_eval(data["moves"])
            if data["moves"] in available_moves
            else None
        )
        return ast.literal_eval(class_name)(**data)

    def __eq__(self, other):
        """Check whether other equals self elementwise."""
        if not isinstance(other, Player):
            return False
        attr_keys = self.__dict__.keys()
        return all(
            self.__getattribute__(key) == other.__getattribute__(key)
            for key in attr_keys
        )


class AIPlayer(Player):
    """Player class for an AI-managed player."""

    def __init__(
        self,
        mark: int,
        name: str,
        moves: Optional[Callable[[List[List[int]], int], Tuple[int, int]]] = naive_move,
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

    def ask_move(self, grid: List[List[int]]) -> Optional[Tuple[int, int]]:
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
        moves: Optional[Callable[[List[List[int]], int], Tuple[int, int]]] = None,
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

    def ask_move(self, grid: List[List[int]]) -> Optional[Tuple[int, int]]:
        """Asks the player what move he wants to play."""
        if self.moves is not None:
            return self.moves(grid, self.get_mark())
        return None


class PlayersMatch:
    """Matches players together and manages turns.

    Attributes:
        players: tuple(Player, Player), Players playing against each other.
        current_player: Player, Holds the player currently playing.
    """

    def __init__(self, player_x: Player, player_o: Player) -> None:
        """Constructor.

        Args:
            player_x: Player, Player with the "X" mark. Will begin game.
            player_o: Player, Player with the "Y" mark.
        """
        self.players: Tuple[Player, Player] = (player_x, player_o)

        # Holds the player currently playing. Rules dictate that "X" starts the game.
        self.current_player: Player = player_x

    def update_ai_algorithm(
        self, algorithm: Callable[[List[List[int]], int], Tuple[int, int]]
    ) -> None:
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

    def to_dict(self) -> Dict[str, Any]:
        """Converts the PlayersMatch instance to a dictionary."""
        return dict(
            players=[player.to_dict() for player in self.players],
            current_player=self.current_player.to_dict(),
            __class=self.__class__.__name__,
        )

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "PlayersMatch":
        """Constructs PlayersMatch instance from dictionary."""
        players = [Player.from_dict(player) for player in data.get("players")]
        current_player = Player.from_dict(data.get("current_player"))
        players_match = PlayersMatch(*players)
        if players_match.current() != current_player:
            players_match.switch()
        return players_match

    def __eq__(self, other: "PlayersMatch"):
        """Check whether other equals self elementwise."""
        if not isinstance(other, PlayersMatch):
            return False
        attr_keys = self.__dict__.keys()
        return all(
            self.__getattribute__(key) == other.__getattribute__(key)
            for key in attr_keys
        )


class Engine:
    """Engine.

    Attributes:
        board: Board, The current board being played.
    """

    def __init__(self, players_match: PlayersMatch, board: Board) -> None:
        """Returns a Game instance initialized with players params."""
        self.players_match = players_match
        self.board = board

    def get_move(self) -> Optional[Tuple[int, int]]:
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

    def __repr__(self) -> str:
        """Returns instance representation."""
        return f"{self.__class__.__name__}({self.players_match!r}, {self.board!r})"

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Engine instance to a dictionary."""
        return dict(
            players_match=self.players_match.to_dict(),
            board=self.board.to_dict(),
            __class=self.__class__.__name__,
        )

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Engine":
        """Constructs Engine instance from dictionary."""
        return Engine(data.get("players_match"), data.get("board"))

    def __eq__(self, other: "Engine"):
        """Check whether other equals self elementwise."""
        if not isinstance(other, Engine):
            return False
        attr_keys = self.__dict__.keys()
        return all(
            self.__getattribute__(key) == other.__getattribute__(key)
            for key in attr_keys
        )


MODE = Literal["single", "multi"]


def build_game(
    player_1_name: Optional[str] = None,
    player_2_name: Optional[str] = None,
    player_1_starts: bool = True,
    mode: MODE = "single",
) -> Engine:
    """Returns a game object."""
    player_1_mark = 1 if player_1_starts is True else -1
    player_1: Player = HumanPlayer(player_1_mark, player_1_name or "Player 1")

    player_2_mark = 0 - player_1_mark
    player_2: Player
    if mode == "single":
        player_2 = AIPlayer(player_2_mark, player_2_name or "Bot")
    else:
        player_2 = HumanPlayer(player_2_mark, player_2_name or "Player 2")

    return Engine(PlayersMatch(player_1, player_2), Board())
