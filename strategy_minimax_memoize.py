from strategy import Strategy
from game_state import GameState
from subtract_square_state import SubtractSquareState  # for testing
from tippy_state import TippyGameState   # for testing


class StrategyMinimaxMemoize(Strategy):
    """
    Interface to suggest move based on the strategy minimax. Memoize
    the score of each GameState to avoid redundency. Override the __init__
    method of class Strategy.

    TO_WIN: float -- corresponds to score 1.0, the player is guaranteed to win
    TO_LOSE: float -- corresponds to score -1.0, the opponent is guaranteed
                      to win
    TO_TIE: float -- the game is going to tie
    """
    TO_WIN, TO_LOSE, TO_TIE = 1.0, -1.0, 0.0

    def __init__(self, interactive=False):
        """(StrategyMinimaxMemoize, bool) -> NoneType

        Create new StrategyMinimaxMemoize (self), prompt user if interactive.
        memo is a dictionary whose keys are strings of GameState and the
        corresponding values are their minimax scores for the next player
        (the computer).
        """
        self.memo = {}

# I implemented memoization in the function below,
    def get_score(self, state):
        """(StrategyMinimaxMemoize, GameState) -> float

        Return the score of state for the next player.
        Memoize the score of Gamestates, and store them in self.memo

        >>> state = SubtractSquareState('p1', current_total=2)
        >>> s = StrategyMinimaxMemoize()
        >>> s.get_score(state)
        1.0
        """
        if not str(state) in self.memo:
            if state.over:
                if state.winner(state.next_player):
                    self.memo[str(state)] = StrategyMinimaxMemoize.TO_WIN
                elif state.winner(state.opponent()):
                    self.memo[str(state)] = StrategyMinimaxMemoize.TO_LOSE
                else:
                    self.memo[str(state)] = StrategyMinimaxMemoize.TO_TIE
            else:
                next_states = [state.apply_move(x) for x in
                               state.possible_next_moves()]
                self.memo[str(state)] = max([(-1) * self.get_score(y)
                                             for y in next_states])
        return self.memo[str(state)]

    def bundle_score(self, state):
        """(StrategyMinimaxMemoize, GameState) -> dict(float: list of Move)

        Return a dictionary whose key are class constants TO_WIN, TO_LOSE
        and TO_TIE; their values are lists of Move that lead to these
        scores

        >>> state = SubtractSquareState('p1', current_total=4)
        >>> s = StrategyMinimaxMemoize()
        >>> s.bundle_score(state)
        {-1.0: [SubtractSquareMove(1)], 1.0: [SubtracSquareMove(4)]}
        """
        result = {}
        for move in state.possible_next_moves():
            score = (-1) * self.get_score(state.apply_move(move))
            if score in result:
                result[score].append(move)
            else:
                result[score] = [move]
        return result

    def suggest_move(self, state):
        """(StrategyMinimaxMemoize, GameState) -> Move

        Return a legal move that leads to the highest score for the
        next player. We choose the first element in the list of moves
        that leads to the highest score.

        Overrides Strategy.suggest_move

        >>> state = SubtractSquareState('p1', current_total=4)
        >>> s = StrategyMinimaxMemoize()
        >>> s.suggest_move(state)
        SubtractSquareMove(4)
        """
        bundled_score = self.bundle_score(state)
        highest_score = max(bundled_score.keys())
        return bundled_score[highest_score][0]
                
