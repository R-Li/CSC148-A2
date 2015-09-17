from strategy import Strategy
from game_state import GameState
from subtract_square_state import SubtractSquareState  # for testing
from tippy_state import TippyGameState   # for testing


class StrategyMinimaxPrune(Strategy):
    """
    Interface to suggest move based on the strategy minimax, incorporated
    with he pruning technique

    TO_WIN: float -- corresponds to score 1.0, the player is guaranteed to win
    TO_LOSE: float -- corresponds to score -1.0, the opponent is guaranteed
                      to win
    TO_TIE: float -- the game is going to tie
    """
    TO_WIN, TO_LOSE, TO_TIE = 1.0, -1.0, 0.0
    
    def get_score(self, state, least=TO_LOSE):
        """(StrategyMinimaxPrune, GameState, float) -> float

        Return the score of next player, as defined in minimax strategy,
        using pruning technique. We avoid investigating moves that do not
        change the result. To implement this, we stop investing the move when
        we find a score that is greater than or equal to (-1) * least.

        >>> state = SubtractSquareState('p1', current_total=2)
        >>> s = StrategyMinimaxPrune()
        >>> s.get_score(state)
        1.0
        """
        if state.over:
            if state.winner(state.next_player):
                return StrategyMinimaxPrune.TO_WIN
            elif state.winner(state.opponent()):
                return StrategyMinimaxPrune.TO_LOSE
            else:
                return StrategyMinimaxPrune.TO_TIE
        else:
            guaranteed = StrategyMinimaxPrune.TO_LOSE
            for move in state.possible_next_moves():
                next_state = state.apply_move(move)
                next_score = (-1) * self.get_score(next_state, guaranteed)
                if next_score > guaranteed:
                    guaranteed = next_score  # update guaranteed score
                if guaranteed >= (-1) * least:
                    break   # because keep going does not change the result
            return guaranteed

    def suggest_move(self, state):
        """(StrategyMinimaxPrune, GameState) -> Move

        Return a legal move that leads to the highest score for the
        next player. If find a move that lead to a winning state,
        return that move immediately.

        Overrides Strategy.suggest_move

        >>> state = SubtractSquareState('p1', current_total=4)
        >>> s = StrategyMinimaxPrune()
        >>> s.suggest_move(state)
        SubtractSquareMove(4)
        """
        tie_moves = []  # a list used to store moves leading to a tie
        for move in state.possible_next_moves():
            score = (-1) * self.get_score(state.apply_move(move))
            if score == StrategyMinimaxPrune.TO_WIN:
                return move
            elif score == StrategyMinimaxPrune.TO_TIE:
                tie_moves.append(move)
        if tie_moves == []:  # no strategy to win or tie
            return state.possible_next_moves()[0]
        else:
            return tie_moves[0]
                
