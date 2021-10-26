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
# Standard library imports
import random
from typing import List
from typing import Optional
from typing import Tuple

# Third-party imports

# Local imports


class Grid:
    """Grid class.

    Attributes:
        grid: A 3*3 matrix of string values.
    """

    _empty_cell = "_"
    _vertical_separator = "│"
    _horizontal_separator = "─"
    _intersection = "┼"
    _empty_grid = [["_"] * 3 for row in range(3)]

    def __init__(self) -> None:
        """Inits Grid with an empty grid."""
        self.grid: List[List[str]] = Grid._empty_grid

    def get_cell(self, coord: Tuple[int, int]) -> str:
        """Returns value for cell located at `coord`."""
        return self.grid[coord[0]][coord[1]]

    def set_cell(self, coord: Tuple[int, int], value: str) -> None:
        """Sets `value` for cell located at `coord` if cell is empty."""
        coord_x, coord_y = coord
        if not self.is_empty_cell(coord):
            raise ValueError("This cell has already been played!")
        self.grid[coord_x][coord_y] = value

    def is_empty_cell(self, coord: Tuple[int, int]) -> bool:
        """Checks if cell located at `coord` is empty."""
        return self.get_cell(coord) == Grid._empty_cell

    def is_full(self) -> bool:
        """Checks if grid is full. Gris is full if there is no empty cell left."""
        return not any(
            self.is_empty_cell((irow, icol))
            for irow, row in enumerate(self.grid)
            for icol, col in enumerate(row)
        )

    def is_winning_move(self, coord: Tuple[int, int], value: str) -> bool:
        """Checks if playing `value` at `coord` leads to a win.

        Only checks the combinations containing the cell with the given coordinates.
        Checks the one row, the one column and eventually the two diagonals.
        """
        has_winning_row = all(col == value for col in self.grid[coord[0]])
        has_winning_col = all(row[coord[1]] == value for row in self.grid)

        has_winning_diag = False
        if coord[0] == coord[1]:
            has_winning_diag = all(
                self.grid[irow][irow] == value for irow, row in enumerate(self.grid)
            )
        if coord[0] + coord[1] == 2:
            has_winning_diag = has_winning_diag or all(
                self.grid[2 - irow][irow] == value for irow, row in enumerate(self.grid)
            )
        return bool(has_winning_row or has_winning_col or has_winning_diag)

    def random_available_cell(self) -> Tuple[int, int]:
        """Returns a randomly picked cell among available cells.

        Returns:
            A tuple of (row_index, column_index).
            row_index: int, index of the chosen cell's row.
            column_index: int, index of the chosen cell's column.
        """
        empty_cells = [
            (irow, icol)
            for irow, row in enumerate(self.grid)
            for icol, cell in enumerate(row)
            if self.is_empty_cell((irow, icol))
        ]
        return random.choice(empty_cells)

    def framed_grid(self) -> str:
        """Returns the grid with an additional frame to facilitate reading."""
        framed = []
        for idx, row in enumerate(self.grid):
            framed.append(Grid._vertical_separator.join(row))
            if idx != len(self.grid) - 1:
                framed.append(Grid._intersection.join(Grid._horizontal_separator * 3))
        return "\n".join(framed)

    def __repr__(self) -> str:
        """Returns instance representation."""
        return f"{self.__class__.__name__}({self.grid!r})"


class Player:
    """Base Player class.

    Attributes:
        name: The name of the player.
        mark: The value of the mark currently used. Must be "X" or "O".
    """

    def __init__(self, name: str) -> None:
        """Constructor.

        Args:
            name: str, name of the player.
        """
        self.name = name
        self.mark: Optional[str] = None

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

    def __repr__(self) -> str:
        """Returns instance representation."""
        return f"{self.__class__.__name__}({self.name!r}, {self.mark!r})"


class AIPlayer(Player):
    """Player class for an AI-managed player."""

    def __init__(self, name: str = "Botybot") -> None:
        """Constructor.

        Args:
            name: str, name of the player.
        """
        super().__init__(name=name)


class HumanPlayer(Player):
    """Player class for an AI-managed player."""

    def __init__(self, name: str = "Human") -> None:
        """Constructor.

        Args:
            name: str, name of the player.
        """
        super().__init__(name=name)


class Game:
    """Game class.

    Attributes:
        player_x: Player, Player with the "X" mark. Will begin game.
        player_o: Player, Player with the "Y" mark.
        current_player: Player, Holds the player currently playing.
        grid: Grid, The current grid being played.
    """

    def __init__(self, player_x: Player, player_o: Player) -> None:
        """Constructor.

        Args:
            player_x: Player, Player with the "X" mark. Will begin game.
            player_o: Player, Player with the "Y" mark.
        """
        self.player_x = player_x
        self.player_o = player_o

        # Holds the player currently playing.
        self.current_player: Player = self.player_x

        # Initialize an empty grid.
        self.grid: Grid = Grid()

    def switch_player(self) -> None:
        """Updates `current_player` with the other player."""
        if self.current_player == self.player_x:
            self.current_player = self.player_o
        else:
            self.current_player = self.player_x

    def get_player(self) -> Player:
        """Returns `current_player`."""
        return self.current_player

    def __repr__(self) -> str:
        """Returns instance representation."""
        return (
            f"{self.__class__.__name__}"
            f"({self.player_x!r}, {self.player_o!r}, {self.current_player!r}, "
            f"{self.grid!r})"
        )
