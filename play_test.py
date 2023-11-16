from othello.OthelloGame import *
from othello.bots.Random import BOT as RandomBOT
from othello.bots.mcts_pure import MCTS_BOT as MCTS_PureBOT
from othello.bots.mcts_eq_board import MCTS_BOT as MCTS_EqBoardBOT


board_size=12
def self_play(black, white, verbose=True):
    g = OthelloGame(n=board_size)
    result = g.play(black, white, verbose)
    return result

def main():
    n_game = 100
    bot1_win = 0
    bot2_win = 0
    bot1_name = "p1"
    bot1 = MCTS_EqBoardBOT(c_uct=3, n_playout=300, n=board_size, time_limit=2, name=bot1_name)

    bot2_name = "p2"
    bot2 = MCTS_PureBOT(c_uct=3, n_playout=300, n=board_size, time_limit=2, name=bot2_name)

    for i in range(n_game):
        print("Game {}".format(i+1))
        result = self_play(bot1, bot2, verbose=False)
        if result == BLACK:
            bot1_win += 1
        elif result == WHITE:
            bot2_win += 1

        result = self_play(bot2, bot1, verbose=False)
        if result == BLACK:
            bot2_win += 1
        elif result == WHITE:
            bot1_win += 1

        print("{} win: {}".format(bot1_name, bot1_win))
        print("{} win: {}".format(bot2_name, bot2_win))
        print("----------------------------------------------------------------------------")
if __name__ == '__main__':

    main()
