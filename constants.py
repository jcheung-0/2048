NUM_CELLS = 4
HEADER_LAYERS = 2

# units in pixels
DISPLAY_HEIGHT = 500
DISPLAY_WIDTH = 400
BOARD_SIZE = 400
CELL_PAD = 10
HEADER_PAD = 20
HEADER_HEIGHT = DISPLAY_HEIGHT - BOARD_SIZE

TILE_BACKGROUND_COLORS = {0: "#9e948a", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
                         16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
                         128: "#edcf72", 256: "#edcc61", 512: "#edc850",
                         1024: "#edc53f", 2048: "#edc22e",

                         4096: "#776e65", 8192: "#edc22e", 16384: "#f2b179",
                         32768: "#f59563", 65536: "#f67c5f", }

TILE_TEXT_COLORS = {0: "#9e948a", 2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2",
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2",
                   256: "#f9f6f2", 512: "#f9f6f2", 1024: "#f9f6f2",
                   2048: "#f9f6f2",

                   4096: "#eee4da", 8192: "#f9f6f2", 16384: "#776e65",
                   32768: "#776e65", 65536: "#f9f6f2", }

# note that 0 has the same background and text color as EMPTY_CELL_COLOR

TILE_FONT = ("Verdana", 40, "bold")

BOARD_BACKGROUND_COLOR = "#92877d"
EMPTY_CELL_COLOR = "#9e948a"

TITLE_FONT = ("Verdana", 50, "bold")
MESSAGE_FONT = ("Verdana", 18, "bold")
HEADER_BACKGROUND_COLOR = "#FFFFFF"
HEADER_TEXT_COLOR = "#776e60"

SCORE_FONT = ("Verdana", 20, "bold")
SCORE_BACKGROUND_COLOR = "#9e948a"
SCORE_TEXT_COLOR = "#eee4da"

RESTART_FONT = ("Verdana", 15, "bold")
RESTART_BACKGROUND_COLOR = "#FFFFFF"
RESTART_TEXT_COLOR = "#776e60"

KEY_UP = "w"
KEY_LEFT = "a"
KEY_DOWN = "s"
KEY_RIGHT = "d"
KEY_RESTART = "r"

NEW_TILES = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]  # a normal game has nine 2's and one 4