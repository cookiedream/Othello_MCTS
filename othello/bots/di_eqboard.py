# -*- coding: utf-8 -*-
"""
A pure implementation of the Monte Carlo Tree Search (MCTS)

@author: Junxiao Song
"""

import numpy as np
import time
#from othello.OthelloUtil import *
from othello.CY_OthelloUtil import *
from othello.OthelloGame import *
import pickle
import hashlib


def get_hash(board: OthelloGame):
    hash_func = hashlib.sha256()
    board_hash = []

    for i in range(8):
        
        new_board = np.rot90(board, i%4, axes=(0,1))
        if i >= 4:
            new_board = np.flip(new_board,axis=1)
        
        board_hash.append(new_board.tobytes())
    
    board_hash.sort()
    board_hash.append(str(board.current_player))
    
    hash_func.update(str(board_hash).encode()) 
    return hash_func.hexdigest()

board_table = {}

def minimax(board: OthelloGame, depth, max_depth, mycolor, start_time):


class MiniMaxBOT(object):
    """AI player based on MCTS"""
    def __init__(self, c_uct=5, n_playout=50, n=8, time_limit=3, name="MCTS"):
     
        self.n = n  
        self.board = OthelloGame(n)
        self.player = None
        self.name = name

            
    def getAction(self, new_board, mycolor):
        
        start_time = time.time()
        self.player = mycolor # 設定我方顏色

        self.board[:] = new_board[:]
        self.board.current_player = self.player
  
        #print(self.board.showBoard())
        #print("hash:", get_hash(self.board))
        # action = self.board.availables()
        # self.board.move((action[1][0], action[1][1]))
        # print(self.board.showBoard())
        # print("hash:", get_hash(self.board))
        #exit()
        self.mcts.reset_root(mycolor, get_hash(self.board))
        
        move = self.mcts.get_move(self.board, start_time) # 取得MCTS的落子(int)
        move_pos = (move//self.n, move%self.n)
        self.board.move(move_pos) # 更新盤面(我方落子)

        return move_pos

    def __str__(self):
        return "MCTS {}".format(self.player)
