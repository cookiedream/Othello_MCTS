# cython: language_level=3

import numpy as np
cimport numpy as np
cimport cython

ctypedef np.int_t DTYPE_t


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
cpdef getValidMoves(np.ndarray[DTYPE_t, ndim=2] board, int color):
    cdef set moves = set()
    cdef int y, x, ydir, xdir, size
    cdef Py_ssize_t dir_idx, color_idx
    cdef Py_ssize_t len_color_positions, board_size, flips_count
    cdef int[:] color_positions_y, color_positions_x 
    cdef tuple positions
    cdef int[:, :] directions = np.array([[1, 1], [1, 0], [1, -1], [0, -1],
                                          [-1, -1], [-1, 0], [-1, 1], [0, 1]], dtype=np.int32)

    board_size = len(board)
    # 找出所有該顏色的棋子位置
    positions = np.where(board == color)
    color_positions_y, color_positions_x = positions[0].astype(np.int32), positions[1].astype(np.int32)
    len_color_positions = len(color_positions_y)

    for color_idx in range(len_color_positions):
        y = color_positions_y[color_idx]
        x = color_positions_x[color_idx]
        # 檢查八個方向
        for dir_idx in range(8):
            flips_count = 0
            for size in range(1, board_size):
                ydir = y + directions[dir_idx][1] * size
                xdir = x + directions[dir_idx][0] * size
                
                if 0 <= xdir < board_size and 0 <= ydir < board_size:
                    if board[ydir, xdir] == -color:
                        flips_count += 1

                    elif board[ydir, xdir] == 0:
                        if flips_count > 0:
                            moves.add((ydir, xdir))
                        break
                    else:
                        break
                else:
                    break
    return np.array(list(moves))

cpdef isValidMove(np.ndarray[DTYPE_t, ndim=2] board, int color, position):
    cdef np.ndarray[DTYPE_t, ndim=2] valids = getValidMoves(board, color)
    cdef int i

    for i in range(valids.shape[0]):
        if (valids[i] == np.array(position)).all():
            return True
    return False

cpdef executeMove(np.ndarray[DTYPE_t, ndim=2] board, int color, position):
    cdef int y, x, ydir, xdir, size
    cdef int[:,:] flips
    cdef Py_ssize_t flips_idx
    cdef Py_ssize_t board_size, flips_count
    
    y, x = position
    board[y, x] = color

    board_size = len(board)

    flips = np.ones((board_size,2), dtype=np.int32) * -1
    for direction in ((1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)):
        flips_count = 0
        for size in range(1, board_size):
            ydir = y + direction[1] * size
            xdir = x + direction[0] * size

            if 0 <= xdir < board_size and 0 <= ydir < board_size:
                if board[ydir, xdir] == -color:
                    flips[flips_count, 0] = ydir
                    flips[flips_count, 1] = xdir
                    flips_count += 1
                # 找到第一個同色的棋子，將中間的棋子翻轉
                elif board[ydir, xdir] == color:
                    for flips_idx in range(flips_count):
                        board[flips[flips_idx, 0], flips[flips_idx, 1]] = color
                    break
                else:
                    break
            else:
                break

cpdef find_oppo_move(np.ndarray[DTYPE_t, ndim=2] old_board, np.ndarray[DTYPE_t, ndim=2] new_board, int mycolor):
    cdef list oppo_moves = []
    cdef int y, x
    cdef Py_ssize_t board_size = len(old_board)
   
    for pos in range(board_size * board_size):
        y = pos // board_size
        x = pos % board_size
        if old_board[y, x] == 0 and new_board[y, x] == -mycolor:
            oppo_moves.append(pos)

    return oppo_moves


cpdef board_2_str(np.ndarray[DTYPE_t, ndim=2] board):
    return ','.join(board.flatten().astype(str))

cpdef isEndGame(np.ndarray[DTYPE_t, ndim=2] board):

    cdef int white_count, black_count

    valid_moves_white = getValidMoves(board, 1)
    valid_moves_black = getValidMoves(board, -1)

    if valid_moves_white.shape[0] == 0 and valid_moves_black.shape[0] == 0:
        white_count = np.sum(board == 1)
        black_count = np.sum(board == -1)

        if white_count > black_count:
            return -1
        elif black_count > white_count:
            return 1
        else:
            return 0
    else:
        return None
