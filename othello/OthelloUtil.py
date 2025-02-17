import numpy as np
from othello import OthelloGame

def getValidMoves(board, color):
    moves = set()

    for y, x in zip(*np.where(board == color)): # 取得所有盤面上color的座標
        # 搜尋每個方向並檢查是否為合法步
        for direction in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
            flips = []
            for size in range(1, len(board)):
                ydir = y + direction[1] * size
                xdir = x + direction[0] * size
                if xdir >= 0 and xdir < len(board) and ydir >= 0 and ydir < len(board):
                    if board[ydir][xdir] == -color:
                        flips.append((ydir, xdir))
              
                    elif board[ydir][xdir] == 0:
                        if len(flips) > 0:
                            moves.add((ydir, xdir))
                        break
                    else:
                        break
                else:
                    break
    return np.array(list(moves))


def isValidMove(board, color, position):
    valids=getValidMoves(board, color)
    # 當落座標存在於合法步列表中即為合法
    if len(valids) != 0 and (valids == np.array(position)).all(1).sum() != 0:
        return True
    else:
        return False

def executeMove(board, color, position):
    # 搜尋所有可翻的棋子，並執行翻棋
    y, x = position
    board[y][x] = color
    for direction in [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]:
        flips = []
        valid_route = False
        for size in range(1, len(board)):
            ydir = y + direction[1] * size
            xdir = x + direction[0] * size
            if xdir >= 0 and xdir < len(board) and ydir >= 0 and ydir < len(board):
                if board[ydir][xdir] == -color:
                    flips.append((ydir, xdir))
                elif board[ydir][xdir] == color:
                    if len(flips) > 0:
                        valid_route = True
                    break
                else:
                    break
            else:
                break
        if valid_route:
            board[tuple(zip(*flips))] = color

def np_2_str(position):
    return str(position[0]) + ',' + str(position[1])

def str_2_np(position):
    return np.array([int(position.split(',')[0]), int(position.split(',')[1])])


def find_opp_move(board, current_board, to_str=False):
    # 搜尋對手落子位置
    opp_moves = list()
    for y, x in zip(*np.where(board != current_board)):
        if current_board[y][x] != 0 and board[y][x] == 0:
            if to_str:
                opp_moves.append(np_2_str((y, x)))
            else:
                opp_moves.append((y, x))
    return opp_moves

def judge_next_game(board, current_board):
    for y, x in zip(*np.where(board != current_board)):
        if current_board[y][x] == 0 and board[y][x] != 0:
            return True

def board_2_str(board):
    return ','.join(board.flatten().astype(str))



def isEndGame(board):
    # 當雙方皆無子可落即結束，並計算雙方子數以決定勝負
    white_valid_moves = len(getValidMoves(board, OthelloGame.WHITE))
    black_valid_moves = len(getValidMoves(board, OthelloGame.BLACK))
    if white_valid_moves == 0 and black_valid_moves == 0:
        v, c = np.unique(board, return_counts=True)
        white_count = c[np.where(v == OthelloGame.WHITE)]
        black_count = c[np.where(v == OthelloGame.BLACK)]
        if white_count > black_count:
            return OthelloGame.WHITE
        elif black_count > white_count:
            return OthelloGame.BLACK
        else:
            return 0
    else:
        return None
