"""
file: backend.py

author: Joshua Cheung

brief: handles the computing behind the game
"""
import random
import constants as c

# all "2d arrays" are indexed as [row][col]

def addNewValue(board):
    """adds a new value to an empty cell on the board"""
    emptyCells = findEmptyCells(board)
    if emptyCells != []:
        row, col = random.choice(emptyCells)
        board[row][col] = random.choice(c.NEW_TILES)
    return board


def addValueUpdateScore(board, score):
    """
    adds a new value to an empty cell on the board
    increases the score by the new value
    """
    emptyCells = findEmptyCells(board)
    newValue = random.choice(c.NEW_TILES)
    if emptyCells != []:
        row, col = random.choice(emptyCells)
        board[row][col] = newValue
    return board, score + newValue


def initializeBoard():
    """creates a new board (square 2d array) with 2 non-zero values"""
    board = [[0 for col in range(c.NUM_CELLS)] for row in range(c.NUM_CELLS)]
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

    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            if board[row][col] == 0:
                coord = (row, col)
                output.append(coord)

    return output


###############################################
####### move in a direction and helpers #######
###############################################


def copy(board):
    """ returns a deep copy of board """
    output = [[0 for col in range(c.NUM_CELLS)] for row in range(c.NUM_CELLS)]

    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            output[row][col] = board[row][col]

    return output


def shiftUp(board):
    """
    returns: board where all non-zero elements have 
    been shifted as far up as possible

    note: cells are shifted starting with the top-most cells
    """
    outputBoard = copy(board)
    for row in range(c.NUM_CELLS):

        for col in range(c.NUM_CELLS):
            targetRow = row

            while outputBoard[targetRow - 1][col] == 0: # searches for column to move the current cell
                if targetRow == 0:
                    break
                else:
                    targetRow -= 1

            if targetRow != row:
                outputBoard[targetRow][col] = board[row][col]
                outputBoard[row][col] = 0
    
    return outputBoard


def combineUp(board):
    """
    Combines vertically adjacent tiles that have the same value.

    note: a single tile can only go through 1 change (or no changes)
    """
    outputBoard = copy(board)
    for row in range(c.NUM_CELLS - 1):
        for col in range(c.NUM_CELLS):
            if outputBoard[row][col] == outputBoard[row+1][col]:
                outputBoard[row][col] *= 2
                outputBoard[row + 1][col] = 0
    
    return outputBoard


def reverseColumns(board):
    """
    returns: a rotated version of the board where the
    left-most column becomes the right-most column

    note: requires square board
    """
    maxRow = c.NUM_CELLS - 1
    outputBoard = [[0 for col in range(c.NUM_CELLS)] for row in range(c.NUM_CELLS)]
    
    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            outputBoard[maxRow - row][col] = board[row][col]
    
    return outputBoard


def transpose(board):
    """
    returns: the transpose of the input board
    ie. all columns and rows are "flipped" accross the diagonal

    note: requires square board
    """
    outputBoard = [[0 for col in range(c.NUM_CELLS)] for row in range(c.NUM_CELLS)]

    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            outputBoard[col][row] = board[row][col]

    return outputBoard


def moveUp(board):
    """
    performs upward move

    returns: updated board, 
             bool of if there were any changes to the board
    """
    outputBoard = shiftUp(board)
    outputBoard = combineUp(outputBoard)
    outputBoard = shiftUp(outputBoard) # gets rid of new spaces from combine
    moveMade = outputBoard != board
    return outputBoard, moveMade


def moveDown(board):
    """
    performs downward move

    returns: updated board,
             bool of if there were any changes to the board
    """
    outputBoard = reverseColumns(board)
    outputBoard = moveUp(outputBoard)[0]
    outputBoard = reverseColumns(outputBoard)
    moveMade = outputBoard != board
    return outputBoard, moveMade


def moveLeft(board):
    """
    performs leftward move

    returns: updated board, 
             bool of if there were any changes to the board
    """
    outputBoard = transpose(board)
    outputBoard = moveUp(outputBoard)[0]
    outputBoard = transpose(outputBoard)
    moveMade = outputBoard != board
    return outputBoard, moveMade


def moveRight(board):
    """
    performs rightward move

    returns: updated board,
             bool of if there were any changes to the board
    """
    outputBoard = transpose(board)
    outputBoard = reverseColumns(outputBoard)
    outputBoard = moveUp(outputBoard)[0]
    outputBoard = reverseColumns(outputBoard)
    outputBoard = transpose(outputBoard)
    moveMade = outputBoard != board
    return outputBoard, moveMade


###################################
##### Check Board Status ##########
###################################

def checkWin(board):
    """checks for a 2048 on the board"""
    for col in board:
        if 2048 in col:
            return True
    return False


def checkLoss(board):
    """
    returns: False if a move can be made
             True otherwise
    """
    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            # an empty cell means we can make a move
            if board[row][col] == 0:
                return False
            
            # if any adjacent cell has same value, then we can combine them
            currentValue = board[row][col]
            
            # check vertically
            if row == 0:
                if board[row+1][col] == currentValue:
                    return False
            elif row == c.NUM_CELLS - 1:
                if board[row-1][col] == currentValue:
                    return False
            else:
                if board[row+1][col] == currentValue:
                    return False
                elif board[row-1][col] == currentValue:
                    return False

            # check horizontally
            if col == 0:
                if board[row][col+1] == currentValue:
                    return False
            elif col == c.NUM_CELLS - 1:
                if board[row][col-1] == currentValue:
                    return False
            else:
                if board[row][col+1] == currentValue:
                    return False
                elif board[row][col-1] == currentValue:
                    return False

    return True


def sumBoard(board):
    """returns the sum of all of the board's values"""
    total = 0
    for row in board:
        for cell in row:
            total += cell
    return total
