import numpy as np
import pygame
import sys
import math

#   Window Dimensions   #
WIDTH = 1000
HEIGHT = 700
WINDOW_SIZE = (WIDTH, HEIGHT)

#   Color Values    #
WHITE = (255, 255, 255)
LIGHTGREY = (160, 160, 160)
GREY = (85, 85, 85)
DARKGREY = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (230, 30, 30)
GREEN = (30, 230, 30)
BLUE = (30, 30, 230)

#   Component Colors   #
BACKGROUND = LIGHTGREY
FOREGROUND = WHITE
CELL_BORDER_COLOR = BLUE
EMPTY_CELL_COLOR = GREY

#   Board Dimensions #
ROW_COUNT = 6
COLUMN_COUNT = 7

#   Component Dimensions    #
SQUARE_SIZE = 100
PIECE_RADIUS = int(SQUARE_SIZE / 2 - 5)

#   Board Coordinates   #
BOARD_BEGIN_X = 30
BOARD_BEGIN_Y = SQUARE_SIZE
BOARD_END_X = BOARD_BEGIN_X + ((COLUMN_COUNT + 1) * SQUARE_SIZE)
BOARD_END_Y = BOARD_BEGIN_Y + (ROW_COUNT * SQUARE_SIZE)

#   Board Dimensions    #
BOARD_WIDTH = BOARD_BEGIN_X + COLUMN_COUNT * SQUARE_SIZE
BOARD_LENGTH = ROW_COUNT * SQUARE_SIZE

#   Player Variables    #
PIECE_COLORS = (GREY, RED, GREEN)
PLAYER1 = 1
PLAYER2 = 2
EMPTY_CELL = 0

#   Game-Dependent Global Variables    #
TURN = 1
GAME_OVER = False


def createBoard(initialCellValue):
    """
    Initializes the game board with the value given.
    :param initialCellValue: Value of initial cell value
    :return: board list with all cells initialized to initialCellValue
    """
    global board
    board = np.full((ROW_COUNT, COLUMN_COUNT), initialCellValue)
    return board


def printBoard():
    """
    Prints the game board to the terminal
    """
    print('\n-\n' +
          str(board) +
          '\n Player ' + str(TURN) + ' plays next')


def drawBoard():
    """
    Draws the game board on the interface with the latest values in the board list
    """
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            col = BOARD_BEGIN_X + (c * SQUARE_SIZE)
            row = BOARD_BEGIN_Y + (r * SQUARE_SIZE)
            piece = board[r][c]
            pygame.draw.rect(
                screen, CELL_BORDER_COLOR, (col, row, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(
                screen, PIECE_COLORS[piece], (int(col + SQUARE_SIZE / 2), int(row + SQUARE_SIZE / 2)), PIECE_RADIUS)
    pygame.display.update()


def hoverPiece():
    """
    Hovers the piece over the game board with the corresponding player's piece color
    """
    pygame.draw.rect(screen, BACKGROUND, (0, BOARD_BEGIN_Y - SQUARE_SIZE, BOARD_WIDTH + SQUARE_SIZE / 2, SQUARE_SIZE))
    posx = pygame.mouse.get_pos()[0]
    if BOARD_BEGIN_X < posx < BOARD_END_X - SQUARE_SIZE:
        pygame.draw.circle(screen, PIECE_COLORS[TURN], (posx, int(SQUARE_SIZE / 2)), PIECE_RADIUS)


def dropPiece(col, piece):
    """
    Drops the given piece in the next available slot in col
    :param col: Column index where the piece will be dropped
    :param piece: Value of the piece to be put in array.
    """
    row = getNextOpenRow(col)
    board[row][col] = piece


def hasEmptySlot(col):
    """
    Checks if current column has an empty slot. Assumes col is within array limits
    :param col: Column index
    :return: True if column has an empty slot. False otherwise.
    """
    return board[0][col] == EMPTY_CELL


def getNextOpenRow(col):
    """
    Gets the next available slot in the column
    :param col: Column index
    :return: If exists, the row of the first available empty slot in the column. None otherwise.
    """
    for r in range(ROW_COUNT - 1, -1, -1):
        if board[r][col] == EMPTY_CELL:
            return r
    return None


def boardIsFull():
    """
    Checks if the board game is full
    :return: True if the board list has no empty slots, False otherwise.
    """
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == 2:
                return False
    return True


def getBoardColumnFromPos(posx):
    """
    Get the index of the board column corresponding to the given position
    :param posx: Position in pixels
    :return: If within board bounds, the index of corresponding column, None otherwise
    """
    column = int(math.floor(posx / SQUARE_SIZE))
    if 0 <= column < COLUMN_COUNT:
        return column
    return None


def switchTurn():
    """
    Switch turns between player 1 and player 2
    """
    global TURN
    if TURN == 1:
        TURN = 2
    else:
        TURN = 1


def gameSession():
    """
    Runs the game session
    """
    global GAME_OVER, TURN
    while not GAME_OVER:
        hoverPiece()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0] - BOARD_BEGIN_X
                column = getBoardColumnFromPos(posx)

                if column is not None:
                    if hasEmptySlot(column):
                        dropPiece(column, TURN)
                        switchTurn()

                        printBoard()
                        drawBoard()

                    GAME_OVER = boardIsFull()


if __name__ == '__main__':
    pygame.init()
    board = createBoard(EMPTY_CELL)

    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill(BACKGROUND)
    drawBoard()

    gameSession()
