"""Tic Tac Toe Game."""
import random
from typing import Tuple, Union, Optional


def game():
    pass


"""Tic Tac Toe Game

Rules:
    The object of Tic Tac Toe is to get three in a row.
    You play on a three by three game board.
    The first player is known as X and the second is O.
    Players alternate placing Xs and Os on the game board,
    until either opponent has three in a row or all nine squares are filled.
    X always goes first, and in the event that no one has three in a row,
    the stalemate is called a cat game.

Version 1.0: Player vs Dumb AI
    Human Player decide if he wants to start or not. Then roles are switched for every game.
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


class Grid:

    _empty_cell = "_"
    _vertical_separator = "│"
    _horizontal_separator = "─"
    _intersection = "┼"
    _empty_grid = [["_"] * 3 for row in range(3)]

    def __init__(self):
        self.grid = Grid._empty_grid

    def get_cell(self, coord: Tuple[int, int]) -> str:
        return self.grid[coord[0]][coord[1]]

    def set_cell(self, coord: Tuple[int, int], value: str) -> None:
        if self.grid[coord[0]][coord[1]] != Grid._empty_cell:
            raise ValueError('This cell has already been played!')
        self.grid[coord[0]][coord[1]] = value

    def is_empty_cell(self, coord: Tuple[int, int]) -> bool:
        return self.get_cell(coord) == Grid._empty_cell

    def is_full(self) -> bool:
        return all(cell != Grid._empty_cell for row in self.grid for cell in row)

    def is_winning_move(self, coord: Tuple[int, int], value: str) -> bool:
        has_winning_row = all(col == value for col in self.grid[coord[0]])
        has_winning_col = all(row[coord[1]] == value for row in self.grid)
        has_winning_diag = False
        if coord[0] == coord[1]:
            has_winning_diag = all(self.grid[irow][irow] == value for irow, row in enumerate(self.grid))
        if coord[0] + coord[1] == 2:
            has_winning_diag = has_winning_diag or all(self.grid[2 - irow][irow] == value for irow, row in enumerate(self.grid))
        return has_winning_row or has_winning_col or has_winning_diag

    def framed_grid(self) -> str:
        framed = []
        for idx, row in enumerate(self.grid):
            framed.append(Grid._vertical_separator.join(row))
            if idx != len(self.grid) - 1:
                framed.append(Grid._intersection.join(Grid._horizontal_separator * 3))
        return "\n".join(framed)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.grid!r})"


class Player:

    def __init__(self, kind: str, name: str):
        self.kind = kind
        self.name = name
        self.mark = None

    def set_mark(self, mark: str) -> None:
        self.mark = mark

    def get_mark(self) -> str:
        return self.mark

    def choose_cell(self, grid: Grid):
        raise NotImplemented

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.kind!r}, {self.name!r}, {self.mark!r})"


class AIPlayer(Player):

    def __init__(self, name: str = "Botybot"):
        super().__init__(kind="AI", name=name)

    def choose_cell(self, grid: Grid) -> Tuple[int, int]:
        empty_cells = [(irow, icol) for irow, row in enumerate(grid.grid)
                       for icol, cell in enumerate(row) if grid.is_empty_cell((irow, icol))]
        random_cell = random.choice(empty_cells)
        return random_cell


class HumanPlayer(Player):

    def __init__(self, name: str = "Human"):
        super().__init__(kind="Human", name=name)


class Game:

    def __init__(self, player_x: Player, player_o: Player):
        self.grid: Grid = Grid()
        self.player_x = player_x
        self.player_o = player_o
        self.current_player: Optional[Player] = None

    def init_game(self):
        pass

    def play_turn(self):
        pass

    def switch_player(self) -> None:
        if not self.current_player:
            self.current_player = self.player_x
        elif self.current_player == self.player_x:
            self.current_player = self.player_o
        else:
            self.current_player = self.player_x

    def get_player(self) -> Player:
        return self.current_player

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.grid!r}, {self.player_x!r}, {self.player_o!r}, {self.current_player!r})"


def play_game():
    pass
