from AIGamePlatform import Othello
#from othello.bots.Random import BOT
from othello.bots.mcts_pure import MCTS_BOT
from othello.bots.mcts_eq_board import MCTS_BOT as MCTS_EqBoardBOT

borad_size=12
print("EQBoard")
app=Othello() # 和平台建立WebSocket連線
bot2=MCTS_EqBoardBOT(c_uct=2, n_playout=250, n=borad_size, time_limit=1) # 建立隨機bot

@app.competition(competition_id='test_TA') # 競賽ID
def _callback_(board, color): # 當需要走步會收到盤面及我方棋種
    # print(board, color)
    return bot2.getAction(board, color) # bot回傳落子座標

