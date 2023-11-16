from AIGamePlatform import Othello
#from othello.bots.Random import BOT
from othello.bots.mcts_pure import MCTS_BOT
from othello.bots.mcts_eq_board import MCTS_BOT as MCTS_EqBoardBOT

borad_size=12

print("MCTS")
app=Othello() # 和平台建立WebSocket連線
bot=MCTS_BOT(c_uct=2.5, n_playout=1300, n=borad_size, time_limit=3.15)


@app.competition(competition_id='112人工智慧導論-複賽') # 競賽ID
def _callback_(board, color): # 當需要走步會收到盤面及我方棋種
    # print(board, color)
    return bot.getAction(board, color) # bot回傳落子座標

