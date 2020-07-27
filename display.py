# file: display.py
#
# author: Joshua Cheung
# based on code from: https://github.com/kiteco/python-youtube-code/tree/master/AI-plays-2048
#
# original code: 
#    Header on top of board
#       update instructions to display a win/loss message when appropriate
#       dynamic score counter
#       reset button
# 
# brief: start and display the game


from tkinter import *
import constants as c
import brain


class Display(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.master.bind("<Key>", self.keyboardInput)

        self.commands = {c.KEY_UP:      brain.moveUp,
                         c.KEY_DOWN:    brain.moveDown,
                         c.KEY_LEFT:    brain.moveLeft,
                         c.KEY_RIGHT:   brain.moveRight,
                         c.KEY_RESTART: self.restart}
        
        # only for testing:
        self.commands["k"] = brain.initializeBoardWin
        self.commands["l"] = brain.initializeBoardLoss
        # end testing commands section

        self.hasWon = False
        self.hasLost = False
        self.createBoard()
        self.score = brain.sumBoard(self.boardValues)
        self.gridCells = [] #indexed as [row][column]
        self.createGrid()
        self.drawGrid()
        self.mainloop()

    def createBoard(self):
        self.boardValues = brain.initializeBoard()

    def createGrid(self):
        headerBackground = Frame(self, bg=c.HEADER_BAGROUND_COLOR,
                                 width=c.DISPLAY_WIDTH, height=c.HEADER_HEIGHT)
        headerBackground.grid(row=0)

        boardBackground = Frame(self, bg=c.BOARD_BACKGROUND_COLOR,
                                width=c.DISPLAY_WIDTH, height=c.BOARD_SIZE)
        boardBackground.grid(row=1)

        for row in range(c.NUM_CELLS + c.HEADER_LAYERS):
            grid_row = []
            for col in range(c.NUM_CELLS):
                    # Start by creating the header. note: the header should span 2 rows
                    if row == 0:
                        if col == 0:  # 2048! Label
                            ##### TODO: label gets cut off at bottom. Need to fix
                            cell = Frame(headerBackground, bg=c.EMPTY_COLOR,
                                         width=int(2/3*c.DISPLAY_WIDTH),
                                         height=(c.HEADER_HEIGHT / c.HEADER_LAYERS))

                            cell.grid(row=row, column=col, rowspan=2)

                            t = Label(master=cell, text="2048!",
                                      anchor="nw", fg=c.HEADER_TEXT_COLOR,
                                      bg=c.HEADER_BAGROUND_COLOR, 
                                      font=("Verdana", 60, "bold"), 
                                      width=12, height=1)
                        
                        elif col == c.NUM_CELLS - 1: # "SCORE" label
                            cell = Frame(headerBackground, bg=c.EMPTY_COLOR,
                                        width=int(c.DISPLAY_WIDTH),
                                        height=(c.HEADER_HEIGHT / c.HEADER_LAYERS))

                            cell.grid(row=row, column=col, padx=5, pady=5)
                            
                            scoreText = "SCORE\n" + str(self.score)
                            t = Label(master=cell, text=scoreText, fg="#eee4da",
                                      bg="#9e948a", justify=CENTER, font=("Verdana", 20, "bold"), 
                                      width=10, height=2, padx=4)

                    elif row == 1:
                        if col == 0: # instructions / win / loss message
                            cell = Frame(headerBackground, bg=c.EMPTY_COLOR,
                                            width=int((2/3)*c.DISPLAY_WIDTH),
                                            height=(c.HEADER_HEIGHT / c.HEADER_LAYERS))

                            cell.grid(row=row, column=col, columnspan=3)

                            t = Label(master=cell, text="Combine the numbers to get the 2048 tile!", 
                                      fg=c.HEADER_TEXT_COLOR, bg=c.HEADER_BAGROUND_COLOR, 
                                      justify=LEFT, font=("Verdana", 18, "bold"),
                                      width=39, height=1, anchor="w")

                        elif col == c.NUM_CELLS - 1: 
                            cell = Button(headerBackground, text="Restart", command=self.restart)
                            cell.grid(row=row, column=col, padx=5, pady=5)

                    else:   # create board
                        cell = Frame(boardBackground, bg=c.EMPTY_COLOR,
                                    width=c.BOARD_SIZE / c.NUM_CELLS,
                                    height=c.BOARD_SIZE / c.NUM_CELLS)
                        
                        cell.grid(row=row, column=col, padx=c.CELL_PAD, pady=c.CELL_PAD)

                        t = Label(master=cell, text="", bg=c.EMPTY_COLOR,
                                justify=CENTER, font=c.TILE_FONT, width=5, height=3)

                    t.grid()
                    grid_row.append(t)

            self.gridCells.append(grid_row)


    def drawGrid(self):
        for row in range(c.HEADER_LAYERS, c.HEADER_LAYERS + c.NUM_CELLS):
            for col in range(len(self.gridCells[row])):
                tileValue = self.boardValues[row - c.HEADER_LAYERS][col]
                self.gridCells[row][col].configure(text=str(tileValue),
                                                     bg=c.TILE_BACKGROUND_COLORS[tileValue],
                                                     fg=c.TILE_TEXT_COLORS[tileValue])
                self.update_idletasks()


    def updateScore(self):
        self.gridCells[0][c.NUM_CELLS - 1].configure(text="SCORE\n" + str(self.score))
        self.update_idletasks()


    def updateWinLoss(self):
        if self.hasLost:
            self.gridCells[1][0].configure(text="Game Over...")
        elif self.hasWon:
            self.gridCells[1][0].configure(text="You Win!")
        else:
            self.gridCells[1][0].configure(text="Combine the numbers to get the 2048 tile!")
        self.update_idletasks()


    def restart(self):
        self.boardValues = brain.initializeBoard()
        self.hasWon = False
        self.hasLost = False
        self.updateWinLoss()
        self.score = brain.sumBoard(self.boardValues)
        self.updateScore()
        self.drawGrid()


    def keyboardInput(self, event):
        key = repr(event.keysym)
        key = key[1] # remove quote marks from key
        key = key.lower()
        if key in self.commands:

            ###### ONLY FOR TESTING DELETE WHEN DONE
            if key in list("kl"): 
                self.boardValues = self.commands[key]()
                self.drawGrid()
            ########################################

            else:
                if key == c.KEY_RESTART:
                    self.restart()
                
                else:
                    self.boardValues, moveMade = self.commands[key](self.boardValues)
                    if moveMade:
                        self.boardValues, self.score = brain.addValueUpdateScore(self.boardValues, self.score)
                        self.drawGrid()
                        self.updateScore()

                        self.hasLost = brain.checkLoss(self.boardValues)
                        if not self.hasWon:
                            self.hasWon = brain.checkWin(self.boardValues)
                        self.updateWinLoss()

                        moveMade = False


if __name__ == "__main__":
    game = Display()