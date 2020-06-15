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
        x, y = random.choice(emptyCells)
        board[x][y] = random.choice(c.NEW_TILES)
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


def moveUp(board):
    print("moveUp called")
    return addNewValue(board)

def moveDown(board):
    return

def moveLeft(board):
    return

def moveRight(board):
    return