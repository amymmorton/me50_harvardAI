"""
Tic Tac Toe Player
"""

import math

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
    if terminal(board):
        return None
    
    if board == initial_state():
        return X
    
    #count number of X and O on the board
    #if X is more than O, then it is O's turn
    x_count = 0
    o_count = 0

    for row in board:
        x_count += row.count(X)
        o_count += row.count(O)

    if x_count > o_count:
        return O
    else:
        return X
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    #end of game - no actions
    if terminal(board):
        return None
    
    #else - all empty cells
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j)) 
    return actions





def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action == None:
        return board
    
    if action not in actions(board):
        raise Exception("Invalid action")
    
    new_board = [[board[i][j] for j in range(3)] for i in range(3)]
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        
    #check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
        
    #check diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]  
    
    #else - no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    #board is full
    if not any(EMPTY in sublist for sublist in board):
        return True

    return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    
    if winner(board) == O:
        return -1   
    
    if winner(board) == None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    #if terminal(board):
    #    return None
    
    #max player, initialize v to negative infinity
    if player(board) == X:

#start of game optimiation- 
        if board == initial_state():
            action = (1,1)
            return action

        v = float("-inf")
        for action in actions(board):
            nextPDepthV = min_value(result(board, action))
            
            if nextPDepthV>v:
                act0 = action #log running best action
            
            v = max(v,nextPDepthV)
            if v == 1:
                return action
        #if no wininning tie or loss- but still need to act
        return act0


    #min player, initialize v to infinity
    if player(board) == O:
        v = float("inf")
        for action in actions(board):
            nextPDepthV = max_value(result(board, action))
        
            #v represents the val of the previous iteration.. log best action if not optimal (above)
            if nextPDepthV < v:
                act0 = action

            v = min(v,nextPDepthV)
            if v == -1:
                return action

        return act0
        


def max_value(board):
    """ calculates the max value of the boards actions available """
    if terminal(board):
        return utility(board)
    
    v = float("-inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v    



def min_value(board):
    if terminal(board):
        return utility(board)
    
    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v    