"""
file: brain.py

author: Joshua Cheung

brief: handles the computing behind the game
"""
import random
import constants as c

# all "2d arrays" are indexed by [row][col]

def addNewValue(board):
    emptyCells = findEmptyCells(board)
    if emptyCells != []:
        row, col = random.choice(emptyCells)
        board[row][col] = random.choice(c.NEW_TILES)
    return board


def addValueUpdateScore(board, score):
    """
    adds new value to board and updates the score
    """
    emptyCells = findEmptyCells(board)
    newValue = random.choice(c.NEW_TILES)
    if emptyCells != []:
        row, col = random.choice(emptyCells)
        board[row][col] = newValue
    return board, score + newValue


def initializeBoard():
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
##### move up/down/left/right and helpers #####
###############################################


def shiftUp(board):
    """
    returns: board where all non-zero elements have 
    been shifted as far left as possible

    note: cells are shifted starting with the left-most cells
    """
    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            targetRow = row

            while board[targetRow - 1][col] == 0: # searches for column to move the current cell
                if targetRow == 0:
                    break
                else:
                    targetRow -= 1

            if targetRow != row:
                board[targetRow][col] = board[row][col]
                board[row][col] = 0
    
    return board        


def combineUp(board):
    for row in range(c.NUM_CELLS - 1):
        for col in range(c.NUM_CELLS):
            if board[row][col] == board[row+1][col]:
                board[row][col] *= 2
                board[row + 1][col] = 0
    
    return board


def reverseColumns(board):
    """
    returns: a rotated version of the board where the
    left-most column becomes the right-most column

    note: requires square board
    """
    maxRow = c.NUM_CELLS - 1
    output = [[0 for col in range(c.NUM_CELLS)] for row in range(c.NUM_CELLS)]
    
    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            output[maxRow - row][col] = board[row][col]
    
    board = output
    return board


def transpose(board):
    """
    returns: the transpose of the input board
    ie. all columns and rows are "flipped"

    note: requires square board
    """
    output = [[0 for col in range(c.NUM_CELLS)] for row in range(c.NUM_CELLS)]

    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            output[col][row] = board[row][col]

    board = output
    return board


def copy(board):
    """
    returns a copy of board
    """
    output = [[0 for col in range(c.NUM_CELLS)] for row in range(c.NUM_CELLS)]

    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            output[row][col] = board[row][col]

    return output


def moveLeft(board):
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
    board = moveUp(board)[0]
    board = transpose(board)
    moveMade = orig != board
    return [board, moveMade]


def moveRight(board):
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
    board = moveUp(board)[0]
    board = reverseColumns(board)
    board = transpose(board)
    moveMade = orig != board
    return [board, moveMade]


def moveUp(board):
    """
    performs leftward move
       - shifts cells left
       - combine pairs of same number
       - shift left again to get rid of any new spaces

    returns:[updated board, 
             bool of if there were any changes to the board]

    note: never do
    board = moveUp(board)
    """
    orig = copy(board)
    board = shiftUp(board)
    board = combineUp(board)
    board = shiftUp(board)
    moveMade = orig != board
    return [board, moveMade]


def moveDown(board):
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
    board = moveUp(board)[0]
    board = reverseColumns(board)
    moveMade = orig != board
    return [board, moveMade]


###################################
##### Check Board Status ##########
###################################

def checkWin(board):
    for col in board:
        if 2048 in col:
            return True

    return False


def checkLoss(board):
    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            # an empty cell means we can make a move
            if board[row][col] == 0:
                return False
            
            # if any adjacent cell has same value, then we can combine them
            currentValue = board[row][col]
            
            # Let's first check horizontally
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

            # Now, let's check vertically

            if col == 0:
                if board[row][col+1] == currentValue:
                    return False
            elif col == c.NUM_CELLS - 1:
                if board[row][col-1] == currentValue:
                    return False
            else:
                if board[row][col+1] == currentValue:
                    return False
                elif board[row-1][col-1] == currentValue:
                    return False
    
    return True


def sumBoard(board):
    total = 0
    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            total += board[row][col]
    return total


######################################
###### Functions for Testing #########
######################################
def printOut(board):
    """
    prints out the board in 2d
    """
    x = transpose(board)
    for col in x:
        print(col)
    x = transpose(board) # resets board if passed into transpose by reference
    return 


def initializeBoardWin():
    board = [[0 for col in range(c.NUM_CELLS)] for row in range(c.NUM_CELLS)]
    board[c.NUM_CELLS - 1][c.NUM_CELLS - 2] = 1024
    board[c.NUM_CELLS - 1][c.NUM_CELLS - 1] = 1024
    return board


def initializeBoardLoss():
    numbers = [2**x for x in range(1,16)]
    numbers.append(0)
    board = [[0 for col in range(c.NUM_CELLS)] for row in range(c.NUM_CELLS)]
    for row in range(c.NUM_CELLS):
        for col in range(c.NUM_CELLS):
            new = random.choice(numbers)
            board[row][col] = new
            numbers.remove(new)
    return board
