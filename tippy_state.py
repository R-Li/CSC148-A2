from game_state import GameState
from tippy_move import TippyMove


class TippyGameState(GameState):
    """The state of a Tippy game

    dimension: int   --- the number of columns of rows of the grid
    grid: list of lists   --- represents a grid with number of rows and columns
                              equal to dimension, the sublists of which are the
                              rows of the grid; the value is 'p1' if the
                              corresponding position is placed (with either
                              cross or circle) by player1,'p2' if it is
                              placed by player2, and 0 if nothing is at that
                              position.
    """

    def __init__(self, p, interactive=False, dimension=3):
        """(TippyGameState, str, bool, int -> NoneType

        Initialize TippyGameState self.

        Assume: p in {'p1', 'p2'} and dimension is an int that >= 3
        """
        if interactive:
            dimension = int(input("How many columns and rows do you"
                                  " want the grid to have:"))
        self.grid = [[0 for i in range(dimension)] for j in range(dimension)]
        GameState.__init__(self, p)
        self.instruction = ("In your turn, you may place a placeholder"
                            " (cross or circle) at a position that has"
                            " not been taken, until you form a tippy")
        self.dimension = dimension
        self.interactive = interactive
        self.over = False
        
    def __repr__(self):
        """(TippyGameState) -> str

        Return a string representation of TippyGameState self
        that evaluates to an equivalent TippyGameState

        >>> t = TippyGameState('p1', True, 5)
        >>> t
        TippyGameState('p1', True, 5)
        """
        return "TippyGameState({}, {}, {})".format(repr(self.next_player),
                                                   repr(self.interactive),
                                                   repr(self.dimension))

    def __str__(self):
        """(TippyGameState) -> str

        Return a convenient string representation of TippyGameState self.

        >>> t = TippyGameState('p1')
        >>> print(t)
        Next player: p1; the checkerboard looks like [[0,0,0],[0,0,0],[0,0,0]]
        """
        return ("Next player: {}; the checkerboard looks like {}".format(
            str(self.next_player), str(self.grid)))

    def __eq__(self, other):
        """(TippyGameState, TippyGameState) -> bool

        Return True iff this TippyGameState is equivalent to other.

        >>> t1 = TippyGameState('p1')
        >>> t2 = TippyGameState('p1', dimension = 3)
        >>> t1 == t2
        True
        """
        return (isinstance(other, TippyGameState) and
                self.next_player == other.next_player and
                self.grid == other.grid)

    def apply_move(self, move):
        """(TippyGameState, TippyMove) -> TippyGameState

        Return the new TippyState reached by applying move to self.

        >>> t1 = TippyState('p2')
        >>> t2 = t1.apply_move(TippyMove((0, 0)))
        >>> t2.grid
        [['p1', 0, 0], [0, 0, 0], [0, 0, 0]]
        >>> t2.next_player
        'p2'
        """
        if move in self.possible_next_moves():
            result = TippyGameState(self.opponent(), 
                                    dimension=self.dimension)
            row = move.position[0]
            col = move.position[1]
            new_grid = [x.copy() for x in self.grid]
            # we do this because the sublists of self.grid are mutable
            new_grid[row][col] = self.next_player
            result.grid = new_grid
            result.over = (True if (result.possible_next_moves() == [] or
                                    contain_tippy('p1', new_grid) or
                                    contain_tippy('p2', new_grid))
                           else False)
            return result
        else:
            return None

    def rough_outcome(self):
        """(TippyGameState) -> float

        Return an estimate in interval [LOSE, WIN] of best outcome next_player
        can guarantee from state self.

        >>> t1 = TippyGameState('p1')
        >>> t1.grid = [['p2', 'p2', 'p1'], ['p1', 'p2', 'p2'], ['p1', 0, 0]]
        >>> t1.rough_outcome()
        -1.0
        >>> t1.grid = [[0, 'p1', 'p2'], ['p2', 'p1', 'p1'], ['p2', 0, 0]]
        >>> t1.rough_outcome()
        1.0
        """
        if contain_tippy(self.opponent(), self.grid):
            return TippyGameState.LOSE
        elif any([contain_tippy(self.next_player, self.apply_move(x).grid)
                  for x in self.possible_next_moves()]):
            return TippyGameState.WIN
        else:
            return TippyGameState.DRAW
            
    def get_move(self):
        """(TippyGameState) -> TippyMove

        Prompt the user and return move.
        """
        position = eval(input("At what position do you want to place"
                              " your placeholder? Please type in this"
                              " format (row number, column number): "))
        # since python count from 0, we subtract 1 from each coordinate
        real_position = (position[0] - 1, position[1] - 1)
        return TippyMove(real_position)

    def winner(self, player):
        """(TippyGameState) -> bool

        Return True iff the game is over and player has won.

        >>> t = TippyGameState('p2')
        >>> t.grid = [['p1', 'p1', 'p2'], ['p2', 'p1', 'p1'], ['p2', 0, 0]]
        >>> t.winner('p1')
        True

        Precondition: player in ['p1', 'p2']
        """
        return contain_tippy(player, self.grid)

    def possible_next_moves(self):
        """(TippyGameState) -> list of TippyMove

        Return a (possibly empty) list of moves that are legal from
        the present state.

        >>> t = TippyGameState('p1', dimension = 5)
        >>> len(t.possible_next_moves())
        25
        """
        result = []
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.grid[i][j] == 0:
                    result.append(TippyMove((i, j)))
        return result
    
# some helper functions:
# let's call the first tippy in A2 instruction type1 tippy;
# it can be shown that a grid contains a tippy iff one of the following holds:
# 1. It contains a type1 tippy
# 2. It contains a type1 tippy after we apply one of the trasnformations below
# 3. It contains a type1 tippy after we apply the composition of the
#    transformations below


def transpose(matrix):
    """(list of lists) -> list of lists

    Return the transpose of matrix.

    >>> m = [[1, 2, 3], [4, 5, 6]]
    >>> transpose(m)
    [[1, 4], [2, 5], [3, 6]]
    """
    result = []
    for i in range(len(matrix[0])):
        result.append([])
        for j in range(len(matrix)):
            result[i].append(matrix[j][i])
    return result
            

def reflection(matrix):
    """(list of lists) -> list of lists

    Return the horizontal reflection of matrix

    >>> m = [[1, 2, 3], [4, 5, 6]]
    >>> reflection(m)
    >>> [[3, 2, 1], [6, 5, 4]]
    """
    result = []
    col = len(matrix[0])
    for row in matrix:
        result.append([])
        for i in range(col):
            result[-1].append(row[-1 - i])
    return result


def check_type1_tippy(p, grid):
    """(str, list of lists) -> bool

    Return True iff grid contains a type1 tippy formed by p

    Assume for this assignment p in ['p1', 'p2']

    >>> grid = [['p1', 'p1', 'p2'], ['p2', 'p1', 'p1'], ['p2', 0, 0]]
    >>> check_type1_tippy('p1', grid)
    True
    """
    col_num = len(grid[0])
    row_num = len(grid)
    # we first check two consecutive p in a row, we do not check the last row
    for i in range(row_num - 1):
        # we do not check the last one and the second last one elements
        # of the row, they cannot be in a type1 tippy
        for j in range(col_num - 2):
            if (grid[i][j] == p and grid[i][j + 1] == p
                    and grid[i + 1][j + 1] == p and grid[i + 1][j + 2] == p):
                return True
    return False


def contain_tippy(p, grid):
    """(str, list of lists) -> bool

    Return True iff grid contains a tippy formed by p

    Assume for this assignment p in ['p1', 'p2']

    >>> grid = [['p2', 'p2', 'p1'], [0, 'p1', 'p1'], [0, 'p1', 'p2']]
    >>> contain_tippy('p1', grid)
    True
    """

    return (check_type1_tippy(p, grid) or
            check_type1_tippy(p, transpose(grid)) or
            check_type1_tippy(p, reflection(grid)) or
            check_type1_tippy(p, reflection(transpose(grid))))
        

