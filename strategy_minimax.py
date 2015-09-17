from strategy import Strategy
from game_state import GameState
from subtract_square_state import SubtractSquareState  # for testing
from tippy_state import TippyGameState   # for testing


class StrategyMinimax(Strategy):
    """
    Interface to suggest move based on the strategy minimax

    TO_WIN: float -- corresponds to score 1.0, the player is guaranteed to win
    TO_LOSE: float -- corresponds to score -1.0, the opponent is guaranteed
                      to win
    TO_TIE: float -- the game is going to tie
    """
    TO_WIN, TO_LOSE, TO_TIE = 1.0, -1.0, 0.0
    
    def get_score(self, state):
        """(StrategyMinimax, GameState) -> int

        Return the score of next player, as defined in minimax strategy.

        >>> state = SubtractSquareState('p1', current_total=2)
        >>> s = StrategyMinimax()
        >>> s.get_score(state)
        1.0
        """
        if state.over:
            if state.winner(state.next_player):
                return StrategyMinimax.TO_WIN
            elif state.winner(state.opponent()):
                return StrategyMinimax.TO_LOSE
            else:
                return StrategyMinimax.TO_TIE
        else:
            next_states = [state.apply_move(x) for x in
                           state.possible_next_moves()]
            return max([(-1) * self.get_score(y) for y in next_states])

    def bundle_score(self, state):
        """(StrategyMinimax, GameState) -> dict(float: list of Move)

        Return a dictionary whose key are class constants TO_WIN, TO_LOSE
        and TO_TIE; their values are lists of Move that lead to these
        scores

        >>> state = SubtractSquareState('p1', current_total=4)
        >>> s = StrategyMinimax()
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
        """(StrategyMinimax, GameState) -> Move

        Return a legal move that leads to the highest score for the
        next player. We choose the first element in the list of moves
        that lead to the highest score.

        Overrides Strategy.suggest_move

        >>> state = SubtractSquareState('p1', current_total=4)
        >>> s = StrategyMinimax()
        >>> s.suggest_move(state)
        SubtractSquareMove(4)
        """
        bundled_score = self.bundle_score(state)
        highest_score = max(bundled_score.keys())
        return bundled_score[highest_score][0]
        
    
