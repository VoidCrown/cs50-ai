"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    emptys = 0
    for row in board:
        for item in row:
            if item is EMPTY:
                emptys += 1
        
    # number of emptys is even, O player times
    if emptys % 2 == 0:
        return O
    # number of emptys is odd, X player times
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    return set((i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY)



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # if action is not a valid action for the board
    if action not in actions(board):
        raise Exception("Invalid action!")
    
    # make sure action could not change the origin board
    new_board = copy.deepcopy(board)
    i, j = action
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    for row in board:
        if all(x == row[0] for x in row) and EMPTY not in row:
            return row[0]
        
    # check columns
    for i in range(3):
        column_itmes = set()
        for j in range(3):
            column_itmes.add(board[j][i])
        if len(column_itmes) == 1 and EMPTY not in column_itmes:
            return column_itmes.pop()
        
    # check diagonal
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[1][1]
    if board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[1][1]

    # no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # terminalled if someone win or there is no empty grid
    if winner(board) is not EMPTY:
        return True
    
    for row in board:
        if EMPTY in row:
            return False
        
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax_old(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    best_action = ()

    # if player is X, choose the max value that can be produced from current state.
    if player(board) == X:
        v = float("-inf")
        for action in actions(board):
            current = minValue(result(board, action))
            # choose the maximal value from minValue that opponent chosen
            if current > v:
                v = current
                best_action = action
        return best_action
    
    # if player is O, choose the min value that can be produced from current state.
    if player(board) == O:
        v = float("inf")
        for action in actions(board):
            current = maxValue(result(board, action))
            # choose the minimal value from maxValue that opponent chosen
            if current < v:
                v = current
                best_action = action
        return best_action


def maxValue(board):
    """
    Returns the max value the given board can produce.
    """
    v = float("-inf")
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, minValue(result(board, action)))
    return v


def minValue(board):
    """
    Returns the min value the given board can produce.
    """
    v = float("inf")
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, maxValue(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    best_action = ()

    # if player is X, choose the max value that can be produced from current state.
    if player(board) == X:
        v = float("-inf")
        for action in actions(board):
            current = alphgaBetaValue(result(board, action), v, -v)
            # choose the maximal value from minValue that opponent chosen
            if current > v:
                v = current
                best_action = action
        return best_action
    
    # if player is O, choose the min value that can be produced from current state.
    if player(board) == O:
        v = float("inf")
        for action in actions(board):
            current = alphgaBetaValue(result(board, action), -v, v)
            # choose the minimal value from maxValue that opponent chosen
            if current < v:
                v = current
                best_action = action
        return best_action
    
    

def alphgaBetaValue(board, alpha, beta):
    """
    Returns the value of optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board)

    if player(board) == X:
        v = float("-inf")
        for action in actions(board):
            v = max(v, alphgaBetaValue(result(board, action), alpha, beta))
            alpha = max(v, alpha)
            if alpha >= beta:
                break
        return v
    else:
        v = float("inf")
        for action in actions(board):
            v = min(v, alphgaBetaValue(result(board, action), alpha, beta))
            beta = min(v, beta)
            if alpha >= beta:
                break
        return v