"""Tic Tac Toe Game."""


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


class Player:

    def __init__(self, kind: str, name: str):
        self.kind = kind
        self.name = name
        self.mark = None

    def set_mark(self, mark):
        self.mark = mark

    def get_mark(self):
        return self.mark


class AIPlayer(Player):

    def __init__(self, name: str = "Botybot"):
        super().__init__(kind="AI", name=name)


class HumanPlayer(Player):

    def __init__(self, name: str = "Human"):
        super().__init__(kind="Human", name=name)


class Grid:

    _empty_cell = "_"
    _vertical_separator = "│"
    _horizontal_separator = "─"
    _intersection = "┼"
    _empty_grid = [["_"] * 3 for row in range(3)]

    def __init__(self):
        self.grid = Grid._empty_grid

    def framed_grid(self):
        framed = []
        for idx, row in enumerate(self.grid):
            framed.append(Grid._vertical_separator.join(row))
            if idx != len(self.grid) - 1:
                framed.append(Grid._intersection.join(Grid._horizontal_separator * 3))
        return "\n".join(framed)

    def __repr__(self):
        return self.framed_grid()

    def __str__(self):
        return self.__repr__()


class Game:

    def __init__(self, player_x: Player, player_o: Player):
        self.grid = Grid()
        self.player_x = player_x
        self.player_o = player_o
        self.current_player = self.player_x

    def init_game(self):
        pass

    def play_turn(self):
        pass

    def get_next_player(self):
        if self.current_player == self.player_x:
            return self.player_o
        else:
            return self.player_x


def play_game():
    pass
