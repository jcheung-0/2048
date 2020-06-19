"""
file: brain.py

author: Joshua Cheung

brief: handles the computing behind the game
"""
import random
import constants as c

def addNewValue(board):
    emptyCells = findEmptyCells(board)
    if emptyCells != []:
        col, row = random.choice(emptyCells)
        board[col][row] = random.choice(c.NEW_TILES)
    return board  


def initializeBoard():
    board = [[0 for row in range(c.NUM_CELLS)] for col in range(c.NUM_CELLS)]
    for i in range(2): # start game with 2 tiles
        board = addNewValue(board)
    return board


def findEmptyCells(board):
    """
    Input: board    - 2d array of cells

    returns: list of coordinates of empty cells, ie. value == o
    each coordinate is a tuple of the form (x, y)
    """
    output = []

    for col in range(c.NUM_CELLS):
        for row in range(c.NUM_CELLS):
            if board[col][row] == 0:
                coord = (col, row)
                output.append(coord)

    return output

###############################################
##### move up/down/left/right and helpers #####
###############################################
def shiftLeft(board):
    """
    returns: board where all non-zero elements have 
    been shifted as far left as possible

    note: cells are shifted starting with the left-most cells
    """
    for col in range(c.NUM_CELLS):
        for row in range(c.NUM_CELLS):
            targetCol = col

            while board[targetCol - 1][row] == 0: # searches for column to move the current cell
                if targetCol == 0:
                    break
                else:
                    targetCol -= 1

            if targetCol != col:
                board[targetCol][row] = board[col][row]
                board[col][row] = 0
    
    return board        


def combineLeft(board):
    for col in range(c.NUM_CELLS - 1):
        for row in range(c.NUM_CELLS):
            if board[col][row] == board[col+1][row]:
                board[col][row] *= 2
                board[col + 1][row] = 0
    
    return board


def reverseColumns(board):
    """
    returns: a rotated version of the board where the
    left-most column becomes the right-most column

    note: requires square board
    """
    maxCol = c.NUM_CELLS - 1
    output = [[0 for row in range(c.NUM_CELLS)] for col in range(c.NUM_CELLS)]
    
    for col in range(c.NUM_CELLS):
        for row in range(c.NUM_CELLS):
            output[maxCol - col][row] = board[col][row]
    
    board = output
    return board


def transpose(board):
    """
    returns: the transpose of the input board
    ie. all columns and rows are "flipped"

    note: requires square board
    """
    output = [[0 for row in range(c.NUM_CELLS)] for col in range(c.NUM_CELLS)]

    for col in range(c.NUM_CELLS):
        for row in range(c.NUM_CELLS):
            output[row][col] = board[col][row]

    board = output
    return board


def copy(board):
    """
    returns a copy of board
    """
    output = [[0 for row in range(c.NUM_CELLS)] for col in range(c.NUM_CELLS)]

    for col in range(c.NUM_CELLS):
        for row in range(c.NUM_CELLS):
            output[col][row] = board[col][row]

    return output


def moveUp(board):
    """
    performs upward move
       - shifts cells up
       - combine pairs of same number
       - shift up again to get rid of any new spaces

    returns:[updated board, 
             bool of if there were any changes to the board]

    note: never do
    board = moveUp(board)
    """
    orig = copy(board)
    board = transpose(board)
    board = moveLeft(board)[0]
    board = transpose(board)
    moveMade = orig != board
    return [board, moveMade]


def moveDown(board):
    """
    performs downward move
       - shifts cells down
       - combine pairs of same number
       - shift down again to get rid of any new spaces

    returns:[updated board, 
             bool of if there were any changes to the board]

    note: never do
    board = moveDown(board)
    """
    orig = copy(board)
    board = transpose(board)
    board = reverseColumns(board)
    board = moveLeft(board)[0]
    board = reverseColumns(board)
    board = transpose(board)
    moveMade = orig != board
    return [board, moveMade]


def moveLeft(board):
    """
    performs leftward move
       - shifts cells left
       - combine pairs of same number
       - shift left again to get rid of any new spaces

    returns:[updated board, 
             bool of if there were any changes to the board]

    note: never do
    board = moveLeft(board)
    """
    orig = copy(board)
    board = shiftLeft(board)
    board = combineLeft(board)
    board = shiftLeft(board)
    moveMade = orig != board
    return [board, moveMade]


def moveRight(board):
    """
    performs rightward move
       - shifts cells right
       - combine pairs of same number
       - shift right again to get rid of any new spaces

    returns:[updated board, 
             bool of if there were any changes to the board]

    note: never do
    board = moveRight(board)
    """
    orig = copy(board)
    board = reverseColumns(board)
    board = moveLeft(board)[0]
    board = reverseColumns(board)
    moveMade = orig != board
    return [board, moveMade]


def checkWin(board):
    for row in board:
        if 2048 in row:
            return True

    return False


def checkLoss(board):
    for row in board:
        if 0 in row:
            return False
    # check if you can combine anything


def printOut(board):
    """
    prints out the board in 2d
    """
    x = transpose(board)
    for row in x:
        print(row)
    x = transpose(board) # resets board if passed into transpose by reference
    return 