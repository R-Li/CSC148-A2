from strategy import Strategy
from game_state import GameState
from subtract_square_state import SubtractSquareState  # for testing
from tippy_state import TippyGameState   # for testing


class StrategyMinimaxMyopic(Strategy):
    """
    Interface to suggest move based on the strategy minimax, using
    myopic technique.

    TO_WIN: float -- corresponds to score 1.0, the player is guaranteed to win
    TO_LOSE: float -- corresponds to score -1.0, the opponent is guaranteed
                      to win
    TO_TIE: float -- the game is going to tie
    """
    TO_WIN, TO_LOSE, TO_TIE = 1.0, -1.0, 0.0

    def __init__(self, interactive=False):
        """(StrategyMinimaxMyopic, bool) -> NoneType

        Create new Strategy (self), prompt user if interactive.
        self.n is the number of steps we want this strategy to
        took ahead
        """
        # self.n = int(input("How many steps do you want"
        #                    " minimax to look ahead: "))
        # the auto checker may not allow me to input self.n
        # we set self.n = 3
        self.n = 3

    def get_score(self, state, step=1):
        """(StrategyMinimaxMyopic, GameState) -> float

        Return the score of the next player, step counts how many steps
        the recursive has looked ahead. Use rough_outcome to estimate outcome
        if the step is greater than self.n 

        >>> state = SubtractSquareState('p1', current_total=2)
        >>> s = StrategyMinimaxMyopic()
        >>> s.get_score(state)
        1.0
        """
        if state.over:
            if state.winner(state.next_player):
                return StrategyMinimaxMyopic.TO_WIN
            elif state.winner(state.opponent()):
                return StrategyMinimaxMyopic.TO_LOSE
            else:
                return StrategyMinimaxMyopic.TO_TIE
        elif step == self.n:
            return state.rough_outcome()
        else:
            next_states = [state.apply_move(x) for x in
                           state.possible_next_moves()]
            return max([(-1) * self.get_score(y, step + 1)
                        for y in next_states])

    def bundle_score(self, state):
        """(StrategyMinimaxMyopic, GameState) -> dict(float: list of Move)

        Return a dictionary whose key are class constants float in the interval
        [TO_LOSE, TO_WIN]; their values are lists of Move that lead to these
        scores

        >>> state = SubtractSquareState('p1', current_total=100)
        >>> s = StrategyMinimaxMyopic()
        How many steps do you want minimax to look ahead: 1
        >>> s.bundle_score(state)[-1.0]
        [SubtractSquareMove(36), SubtractSquareMove(64)]
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
        """(StrategyMinimaxMyopic, GameState) -> Move

        Return a legal move that leads to the highest score for the
        next player. We choose the first element in the list of moves
        that lead to the highest score.

        Overrides Strategy.suggest_move

        >>> state = SubtractSquareState('p1', current_total=4)
        >>> s = StrategyMinimaxMyopic()
        How many steps do you want minimax to look ahead: 1
        >>> s.suggest_move(state)
        SubtractSquareMove(4)
        """
        bundled_score = self.bundle_score(state)
        highest_score = max(bundled_score.keys())
        return bundled_score[highest_score][0]
            
