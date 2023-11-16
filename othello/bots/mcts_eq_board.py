# -*- coding: utf-8 -*-
"""
A pure implementation of the Monte Carlo Tree Search (MCTS)

@author: Junxiao Song
"""

import numpy as np
import time
# from othello.OthelloUtil import *
from othello.CY_OthelloUtil import *
from othello.OthelloGame import *
import pickle
import hashlib


def get_hash(board: OthelloGame):
    hash_func = hashlib.sha256()
    board_hash = []

    for i in range(8):

        new_board = np.rot90(board, i % 4, axes=(0, 1))
        if i >= 4:
            new_board = np.flip(new_board, axis=1)

        board_hash.append(new_board.tobytes())

    board_hash.sort()
    board_hash.append(str(board.current_player))

    hash_func.update(str(board_hash).encode())
    return hash_func.hexdigest()


class TreeNode():

    def __init__(self, parent: "TreeNode", curr_player, player_color, hash_value):
        self._parent = parent
        self._children = {}
        self.children_group = {}

        self._n_visits = 0
        self._Q = 0

        self.hash_value = hash_value
        self.curr_player = curr_player
        self.player_color = player_color

    def expand(self, actions, next_player, board_size, board: OthelloGame):
        """ 展開節點 """
        for act_ind in range(actions.shape[0]):
            action = actions[act_ind][0] * board_size + actions[act_ind][1]

            if action not in self._children:
                # 取得此行動後的盤面hash值
                tmp_board = board.clone()
                tmp_board.move((actions[act_ind][0], actions[act_ind][1]))
                board_hash = get_hash(tmp_board)
                # 建立子節點
                self._children[action] = TreeNode(
                    self, next_player, self.player_color, board_hash)
                # 若hash值相同，則將節點加入同一個group
                if board_hash not in self.children_group:
                    self.children_group[board_hash] = [self._children[action]]
                else:
                    self.children_group[board_hash].append(
                        self._children[action])

    def select(self, c_uct):
        total_visits = sum(
            child._n_visits for child in self._children.values())
        sqrt_total_visits = np.sqrt(total_visits)
        return max(self._children.items(), key=lambda act_node: act_node[1].get_value(c_uct, sqrt_total_visits))

    def get_value(self, c_uct, sqrt_total_visits):
        """ 
            計算UCT值
            c_uct: UCT係數
            return: Q + UCT值
        """
        return self._Q + (c_uct * sqrt_total_visits / (1 + self._n_visits))

    def back_update(self, leaf_value):
        """ 
            反向去更所有直系節點的Q值和訪問次數
            leaf_value: 從葉節點到當前節點的分數(我方的分數，正為我方勝，負為對手勝)
        """

        curr_value = leaf_value
        if self.curr_player != self.player_color:
            curr_value *= -1

        if self.is_root():
            self._n_visits += 1
            self._Q += 1.0 * (curr_value - self._Q) / self._n_visits
        else:

            for child in self._parent.children_group[self.hash_value]:
                child._n_visits += 1
                child._Q += 1.0 * (curr_value - child._Q) / child._n_visits

            self._parent.back_update(leaf_value)

    def is_leaf(self):
        return self._children == {}

    def is_root(self):
        return self._parent is None


class MCTS(object):

    def __init__(self, c_uct=5, n_playout=1000, time_limit=3):

        self._root = None
        self.player_color = None
        self._c_uct = c_uct
        self._n_playout = n_playout
        self.time_limit = time_limit
        self.reset_times = 0

    def reset_root(self, player_color, board_hash_val):
        self.player_color = player_color
        self._root = TreeNode(None, -player_color,
                              player_color, board_hash_val)  # 第一個節點一定是對手的節點

    def _playout(self, state: OthelloGame):
        """
        一次模擬, 會選定一個葉節點, 並從葉節點開始模擬, 會先擴展一次, 直到遊戲結束, 最後更新分數。
        """
        node = self._root
        while (1):
            if node.is_leaf():
                break

            action, node = node.select(self._c_uct)

            state.move((action//state.n, action % state.n))

        # Check for end of game
        end = isEndGame(state)
        if end is None:
            actions = state.availables()

            if actions.shape[0] == 0:
                state.current_player *= -1
                actions = state.availables()

            node.expand(actions, -state.current_player,
                        board_size=state.n, board=state)
            leaf_value = self._rollout(state)

        else:  # 遊戲結束
            leaf_value = end

        leaf_value *= self.player_color  # 轉換成我方的分數
        # 反向更新節點
        node.back_update(leaf_value)

    def _rollout(self, state: OthelloGame):

        while True:
            end = isEndGame(state)
            if end is not None:
                break

            # 遊戲未結束, 隨機選擇一個合法步
            valids = state.availables()  # 取得合法步
            # 若沒有合法步, 換對手走
            if valids.shape[0] == 0:
                state.current_player = -state.current_player
                continue

            act_idx = np.random.choice(valids.shape[0])
            action_pos = valids[act_idx]

            state.move(action_pos)

        return 0 if end == 0 else end * self.player_color

    def get_move(self, board: OthelloGame, start_time):
        # print(board.showBoard())

        for n in range(self._n_playout):

            if time.time() - start_time >= self.time_limit:
                print(f"eq Time out! {n} playouts have been run.")
                break
            self._playout(board.clone())
        # print(f"chlids:[ ", end="")
        # for child in self._root._children.values():
        #     print(f"{child._n_visits}, ", end="")
        # print("]")
        if len(self._root._children) == 0:
            print("No child!")

        return max(self._root._children.items(), key=lambda act_node: act_node[1]._n_visits)[0]

    def update_with_move(self, last_moves, player_color):
        """ 若新的落子之前有模擬過，則更新tree至新的落子, 否則重置tree """
        update = False
        if len(last_moves) == 1:
            self._root = self._root._children[last_moves[0]]
            self._root._parent = None
            update = True

        return update


class MCTS_BOT1(object):
    """AI player based on MCTS"""

    def __init__(self, c_uct=5, n_playout=50, n=8, time_limit=3, name="MCTS"):
        self.mcts = MCTS(c_uct, n_playout, time_limit=time_limit)
        self.n = n
        self.board = OthelloGame(n)
        self.player = None
        self.name = name

    def getAction(self, new_board, mycolor):

        start_time = time.time()
        self.player = mycolor  # 設定我方顏色

        # 設定當前玩家和更新盤面
        self.board[:] = new_board[:]
        self.board.current_player = self.player

        if self.mcts._root is None:
            self.mcts.reset_root(mycolor, get_hash(self.board.clone()))
        else:
            # 根據對手落子更新tree
            # 回傳對手落子的list，裡面為0~n^2-1的整數
            oppo_moves = find_oppo_move(self.board, new_board, mycolor=mycolor)
            if not self.mcts.update_with_move(oppo_moves, mycolor):
                self.mcts.reset_root(mycolor, get_hash(self.board.clone()))

         # 取得MCTS的落子(int)
        move = self.mcts.get_move(self.board, start_time)

        move_pos = (move//self.n, move % self.n)
        self.board.move(move_pos)  # 更新盤面(我方落子)

        self.mcts.update_with_move([move], mycolor)  # 更新tree至當前狀態

        return move_pos

    def __str__(self):
        return "MCTS {}".format(self.player)
