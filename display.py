# file: display.py
#
# author: Joshua Cheung
# based on code from: https://github.com/kiteco/python-youtube-code/tree/master/AI-plays-2048
#
# brief: display the game


from tkinter import Frame, Label, CENTER
import constants as c
import brain


class Display(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title("2048")
        self.master.bind("<Key>", self.keyboardInput)

        self.commands = {c.KEY_UP:brain.moveUp,
                         c.KEY_DOWN: brain.moveDown,
                         c.KEY_LEFT: brain.moveLeft,
                         c.KEY_RIGHT: brain.moveRight}

        self.createBoard()
        print(self.boardValues)
        self.grid = [] # used for the display
        self.createGrid()
        self.drawGrid()

        self.mainloop()

    def createBoard(self):
        self.boardValues = brain.initializeBoard()

    def createGrid(self):
        background = Frame(self, bg=c.BACKGROUND_COLOR,
                           width=c.BOARD_WIDTH, height=c.BOARD_HEIGHT)

        background.grid()

        for row in range(c.NUM_CELLS):
            grid_row = []
            for col in range(c.NUM_CELLS):
                cell = Frame(background, bg=c.ZERO_COLOR,
                             width=c.BOARD_WIDTH / c.NUM_CELLS,
                             height=c.BOARD_HEIGHT / c.NUM_CELLS)
                
                cell.grid(row=row, column=col, padx=c.CELL_PAD, pady=c.CELL_PAD)

                t = Label(master=cell, text="", bg=c.ZERO_COLOR,
                         justify=CENTER, font=c.FONT, width=5, height=2)

                t.grid()
                grid_row.append(t)

            self.grid.append(grid_row)


    def drawGrid(self):
        for row in range(c.NUM_CELLS):
            for col in range(c.NUM_CELLS):
                tileValue = self.boardValues[row][col]
                self.grid[col][row].configure(text=str(tileValue),
                                                     bg=c.TILE_BACKGROUND_COLORS[tileValue],
                                                     fg=c.TILE_TEXT_COLORS[tileValue])
                self.update_idletasks()



    def keyboardInput(self, event):
        key = repr(event.char)
        print(type(key))
        print(type('w'))
        print( "w" in self.commands)
        print(key in self.commands)
        print(key == 'w')
        if key in self.commands: # does not get past here for some reason
            print("good key press")
            self.boardValues, moveMade, _ = self.commands[key](self.boardValues)
            if moveMade:
                self.boardValues = brain.addNewValue(self.boardValues)
                self.createGrid()
                moveMade = False


        print(self.boardValues)



gamegrid = Display()