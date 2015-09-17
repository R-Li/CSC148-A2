class GameView:
    '''
    A game view for a two-player, sequential move, zero-sum,
    perfect-information game.
    '''

    def __init__(self, state, strategy):
        '''(GameView, GameState.__class__,
            Strategy.__class__) -> NoneType

        Create GameView self for game described by state, where
        computer uses given strategy.
        '''
        player = input('Type c if you wish the computer to play first ')
        if player == 'c':
            p = 'p2'
        else:
            p = 'p1'
        self.state = state(p, interactive=True)
        self.strategy = strategy(interactive=True)

    def play(self):
        ''' (GameView) -> NoneType

        Play a game.
        '''
        print(self.state.instructions)
        print(self.state)
        print()
        while not self.state.over:
            if self.state.next_player == 'p1':
                m = self.state.get_move()
                while not m in self.state.possible_next_moves():
                    # The move was illegal.
                    print('Illegal move: {}\nPlease try again.\n'.format(m))
                    print(self.state.instructions)
                    print(self.state)
                    m = self.state.get_move()
                print('You choose: {}'.format(m))
            else:
                # The computer makes a move.
                m = self.strategy.suggest_move(self.state)
                print('The computer chooses: {}'.format(m))
            self.state = self.state.apply_move(m)
            print('New game state: ', str(self.state))
            print()

        if self.state.winner('p2'):
            # p2, the computer, wins
            print('Beat ya!')
        elif self.state.winner('p1'):
            # p1, the human challenger, wins
            print('Congrats -- you won!!')
        else:
            print('We tied...')


if __name__ == '__main__':
    from subtract_square_state import SubtractSquareState
    from tippy_state import TippyGameState
    game_state = ({'s': SubtractSquareState, 't': TippyGameState,})
    from strategy_random import StrategyRandom
    from strategy_minimax import StrategyMinimax
    from strategy_minimax_memoize import StrategyMinimaxMemoize
    from strategy_minimax_prune import StrategyMinimaxPrune
    from strategy_minimax_myopic import StrategyMinimaxMyopic
    strategy = ({'r': StrategyRandom, 'm': StrategyMinimax,
                 'mm': StrategyMinimaxMemoize,
                 'mp': StrategyMinimaxPrune,
                 'my': StrategyMinimaxMyopic})
    g = ''
    while not g in game_state.keys():
        g = input('s to play Subtract Square, t to play Tippy: ')
    s = ''
    while not s in strategy.keys():
        s = input('r for random strategy ,m for minimax '
                  'strategy, mm for minimax memoize, '
                  'mp for minimax prune, my for minimax myopic:')
    GameView(game_state[g], strategy[s]).play()
