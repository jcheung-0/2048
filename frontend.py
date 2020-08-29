"""
file: frontend.py

author: Joshua Cheung
based on code from: https://github.com/kiteco/python-youtube-code/tree/master/AI-plays-2048

my original code: 
   Header on top of board
      update instructions to display a win/loss message when appropriate
      dynamic score counter
      reset button

brief: start and display the game
"""


from tkinter import *
import constants as c
import backend


class Display(Frame):
    def __init__(self):
        """initialize and start the game"""
        # initialize tkinter widgets
        Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.master.bind("<Key>", self.keyboardInput)

        self.commands = {c.KEY_UP:      backend.moveUp,
                         c.KEY_DOWN:    backend.moveDown,
                         c.KEY_LEFT:    backend.moveLeft,
                         c.KEY_RIGHT:   backend.moveRight,
                         c.KEY_RESTART: self.restartGame}

        # board states
        self.hasWon = False     # does not stop game
        self.hasLost = False    # stops game if true
        self.boardValues = backend.initializeBoard()        # indexed as [row][column]
        self.score = backend.sumBoard(self.boardValues)

        # initialize tkinter display 
        self.guiCells = []     # indexed as [row][column]
        self.createGui()
        self.updateBoard()
        self.mainloop()


    def createGui(self):
        """initializes the gui"""
        headerBackground = Frame(self,
                                 bg=c.HEADER_BACKGROUND_COLOR,
                                 width=c.DISPLAY_WIDTH,
                                 height=c.HEADER_HEIGHT)

        headerBackground.grid(row=0,
                              padx=c.HEADER_PAD,
                              pady=(c.HEADER_PAD,0))

        boardBackground = Frame(self,
                                bg=c.BOARD_BACKGROUND_COLOR,
                                width=c.DISPLAY_WIDTH,
                                height=c.BOARD_SIZE)

        boardBackground.grid(row=1,
                             padx=c.HEADER_PAD,
                             pady=(0,c.HEADER_PAD))


        for row in range(c.NUM_CELLS + c.HEADER_LAYERS):
            gui_row = []
            for col in range(c.NUM_CELLS):
                    # Start by creating the header. note: the header should span 2 rows
                    # note: do not make seperate helper functions to create labels / buttons
                    if row == 0:
                        # 2048! Label
                        if col == 0:
                            cell = Frame(master=headerBackground,
                                         bg=c.EMPTY_CELL_COLOR,
                                         width=int(2/3*c.DISPLAY_WIDTH),
                                         height=c.HEADER_HEIGHT / c.HEADER_LAYERS)

                            cell.grid(row=row,
                                      rowspan=2,
                                      column=col)

                            guiText = Label(master=cell,
                                      text="2048!",
                                      anchor="w", 
                                      justify=LEFT,
                                      fg=c.HEADER_TEXT_COLOR,
                                      bg=c.HEADER_BACKGROUND_COLOR,
                                      font=c.TITLE_FONT,
                                      width=14,
                                      height=2)
                        
                        # "SCORE" label
                        elif col == c.NUM_CELLS - 1:
                            cell = Frame(master=headerBackground,
                                         bg=c.EMPTY_CELL_COLOR,
                                         width=int(c.DISPLAY_WIDTH),
                                         height=c.HEADER_HEIGHT / c.HEADER_LAYERS)

                            cell.grid(row=row,
                                      column=col)
                            
                            guiText = Label(master=cell,
                                      text="SCORE\n{}".format(self.score),
                                      fg=c.SCORE_TEXT_COLOR,
                                      bg=c.SCORE_BACKGROUND_COLOR,
                                      font=c.SCORE_FONT, 
                                      width=10,
                                      height=2)

                    elif row == 1:
                        # instructions / win / loss message
                        if col == 0:
                            cell = Frame(master=headerBackground,
                                         bg=c.EMPTY_CELL_COLOR,
                                         width=int((2/3)*c.DISPLAY_WIDTH),
                                         height=(c.HEADER_HEIGHT / c.HEADER_LAYERS))

                            cell.grid(row=row,
                                      column=col,
                                      columnspan=3)

                            guiText = Label(master=cell,
                                      text="Combine the numbers to get the 2048 tile!",
                                      anchor="sw",
                                      fg=c.HEADER_TEXT_COLOR,
                                      bg=c.HEADER_BACKGROUND_COLOR, 
                                      font=c.MESSAGE_FONT,
                                      width=39,
                                      height=1)

                        # restart button
                        elif col == c.NUM_CELLS - 1:
                            cell = Button(master=headerBackground,
                                          text="Restart",
                                          command=self.restartGame,
                                          fg=c.RESTART_TEXT_COLOR,
                                          bg=c.RESTART_BACKGROUND_COLOR,
                                          font=c.RESTART_FONT,
                                          width=10,
                                          height=2)

                            cell.grid(row=row,
                                      column=col)
                    
                    # create board
                    else:
                        cell = Frame(boardBackground,
                                     bg=c.EMPTY_CELL_COLOR,
                                     width=c.BOARD_SIZE / c.NUM_CELLS,
                                     height=c.BOARD_SIZE / c.NUM_CELLS)
                        
                        cell.grid(row=row,
                                  column=col,
                                  padx=c.CELL_PAD,
                                  pady=c.CELL_PAD)

                        guiText = Label(master=cell,
                                  text="",
                                  bg=c.EMPTY_CELL_COLOR,
                                  font=c.TILE_FONT,
                                  width=5,
                                  height=3)

                    guiText.grid()
                    gui_row.append(guiText)

            self.guiCells.append(gui_row)        


    def updateBoard(self):
        """updates the gui to reflect the current values on the board"""
        for row in range(c.HEADER_LAYERS, c.HEADER_LAYERS + c.NUM_CELLS):
            for colIndex, col in enumerate(self.guiCells[row]):
                tileValue = self.boardValues[row - c.HEADER_LAYERS][colIndex]
                col.configure(text=str(tileValue),
                              bg=c.TILE_BACKGROUND_COLORS[tileValue],
                              fg=c.TILE_TEXT_COLORS[tileValue])
                self.update_idletasks()


    def updateScore(self):
        """updates the gui to reflect the current score"""
        self.guiCells[0][-1].configure(text="SCORE\n{}".format(self.score))
        self.update_idletasks()


    def updateWinLoss(self):
        """updates the starting message to reflect the current state of the game""" 
        # update variables
        self.hasLost = backend.checkLoss(self.boardValues)
        if not self.hasWon:
            self.hasWon = backend.checkWin(self.boardValues)
            
        # update gui
        if self.hasLost:
            self.guiCells[1][0].configure(text="Game Over...")
        elif self.hasWon:
            self.guiCells[1][0].configure(text="You Win!")
        else:
            self.guiCells[1][0].configure(text="Combine the numbers to get the 2048 tile!")
        self.update_idletasks()


    def restartGame(self):
        """updates gui and variables to restart the game"""
        self.boardValues = backend.initializeBoard()
        self.updateBoard()

        self.score = backend.sumBoard(self.boardValues)
        self.updateScore()

        self.hasWon = False
        self.hasLost = False
        self.updateWinLoss()
        


    def keyboardInput(self, event):
        """handles keyboard inputs"""
        key = repr(event.keysym)[1] # pulls key without extra quotation marks
        key = key.lower()

        if key in self.commands:
            if key == c.KEY_RESTART:
                self.restartGame()
            
            else:
                self.boardValues, moveMade = self.commands[key](self.boardValues)
                if moveMade:
                    self.boardValues, self.score = backend.addValueUpdateScore(self.boardValues, self.score)
                    self.updateBoard()
                    self.updateScore()
                    self.updateWinLoss()


if __name__ == "__main__":
    game = Display()
