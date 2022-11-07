import numpy as np
import pygame
import sys
import math
import Button as btn
from tkinter import messagebox, simpledialog

#   Window Dimensions   #
WIDTH = 1050
HEIGHT = 700
WINDOW_SIZE = (WIDTH, HEIGHT)

#   Color Values    #
WHITE = (255, 255, 255)
LIGHTGREY = (170, 170, 170)
GREY = (85, 85, 85)
DARKGREY = (50, 50, 50)
DARKER_GREY = (35, 35, 35)
BLACK = (0, 0, 0)
RED = (230, 30, 30)
DARKRED = (150, 0, 0)
GREEN = (30, 230, 30)
BLUE = (30, 30, 122)
CYAN = (30, 230, 230)

#   Component Colors   #
BOARD_LAYOUT_BACKGROUND = DARKGREY
SCREEN_BACKGROUND = LIGHTGREY
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
BOARD_END_X = BOARD_BEGIN_X + (COLUMN_COUNT * SQUARE_SIZE)
BOARD_END_Y = BOARD_BEGIN_Y + (ROW_COUNT * SQUARE_SIZE)

BOARD_LAYOUT_END_X = BOARD_END_X + 2 * BOARD_BEGIN_X

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
player1score = player2score = 0


def setupFrame():
    """
    Initializes the all components in the frame
    """
    global screen, board
    screen = pygame.display.set_mode(WINDOW_SIZE)
    gradientRect(screen, BLACK, GREY, pygame.draw.rect(screen, SCREEN_BACKGROUND, (0, 0, WIDTH, HEIGHT)))
    board = createBoard(EMPTY_CELL)

    pygame.display.set_caption('Smart Connect4 :)')
    drawBoard()
    drawLabels()
    drawButtons()


######   Labels    ######

def drawLabels():
    """
    Draws all labels on the screen
    """
    titleFont = pygame.font.SysFont("Sans Serif", 40, False, True)
    mainLabel = titleFont.render("Smart Connect4", True, WHITE)
    screen.blit(mainLabel, (BOARD_LAYOUT_END_X + 20, 30))

    captionFont = pygame.font.SysFont("Arial", 15)
    player1ScoreCaption = captionFont.render("Player1", True, BLACK)
    player2ScoreCaption = captionFont.render("Player2", True, BLACK)
    screen.blit(player1ScoreCaption, (BOARD_LAYOUT_END_X + 48, 210))
    screen.blit(player2ScoreCaption, (BOARD_LAYOUT_END_X + 170, 210))

    refreshScores()
    refreshStats()


def refreshScores():
    """
    Refreshes the scoreboard
    """
    pygame.draw.rect(screen, BLACK, (BOARD_LAYOUT_END_X + 9, 119, 117, 82), 0)
    player1ScoreSlot = pygame.draw.rect(screen, BOARD_LAYOUT_BACKGROUND,
                                        (BOARD_LAYOUT_END_X + 10, 120, 115, 80))

    pygame.draw.rect(screen, BLACK, (BOARD_LAYOUT_END_X + 134, 119, 117, 82), 0)
    player2ScoreSlot = pygame.draw.rect(screen, BOARD_LAYOUT_BACKGROUND,
                                        (BOARD_LAYOUT_END_X + 135, 120, 115, 80))

    scoreFont = pygame.font.SysFont("Sans Serif", 80)
    player1ScoreCounter = scoreFont.render(str(player1score), True, PIECE_COLORS[1])
    player2ScoreCounter = scoreFont.render(str(player2score), True, PIECE_COLORS[2])

    player1ScoreLength = player2ScoreLength = 2.7
    if player1score > 0:
        player1ScoreLength += math.log(player1score, 10)
    if player2score > 0:
        player2ScoreLength += math.log(player2score, 10)

    screen.blit(player1ScoreCounter,
                (player1ScoreSlot.x + player1ScoreSlot.width / player1ScoreLength, 135))
    screen.blit(player2ScoreCounter,
                (player2ScoreSlot.x + player2ScoreSlot.width / player2ScoreLength, 135))


def refreshStats():
    """
    Refreshes the analysis section
    """
    pygame.draw.rect(screen, BLACK, (BOARD_LAYOUT_END_X + 9, 299, WIDTH - BOARD_LAYOUT_END_X - 18, 337), 0)
    statRect = pygame.draw.rect(screen, GREY,
                                (BOARD_LAYOUT_END_X + 10, 300, WIDTH - BOARD_LAYOUT_END_X - 20, 335))


######   Buttons    ######

def drawButtons():
    """
    Draws all buttons on the screen
    """
    global showStatsButton, contributorsButton
    showStatsButton = btn.Button(
        screen, color=LIGHTGREY,
        x=BOARD_LAYOUT_END_X + 10, y=250,
        width=WIDTH - BOARD_LAYOUT_END_X - 20, height=30, text="Show nerdy stats :D")
    showStatsButton.draw(BLACK)

    contributorsButton = btn.Button(
        screen, color=LIGHTGREY,
        x=BOARD_LAYOUT_END_X + 10, y=650,
        width=WIDTH - BOARD_LAYOUT_END_X - 20, height=30, text="Contributors")
    contributorsButton.draw(BLACK)


######   Game Board  ######

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
    pygame.draw.rect(screen, BLACK, (0, 0, BOARD_LAYOUT_END_X, HEIGHT), 0)
    boardLayout = pygame.draw.rect(
        screen, BOARD_LAYOUT_BACKGROUND, (0, 0, BOARD_LAYOUT_END_X - 1, HEIGHT))
    gradientRect(screen, DARKER_GREY, DARKGREY, boardLayout)
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
    boardLayout = pygame.draw.rect(screen, BOARD_LAYOUT_BACKGROUND,
                                   (0, BOARD_BEGIN_Y - SQUARE_SIZE, BOARD_WIDTH + SQUARE_SIZE / 2, SQUARE_SIZE))
    gradientRect(screen, DARKER_GREY, DARKGREY, boardLayout)
    posx = pygame.mouse.get_pos()[0]
    if BOARD_BEGIN_X < posx < BOARD_END_X:
        pygame.mouse.set_visible(False)
        pygame.draw.circle(screen, PIECE_COLORS[TURN], (posx, int(SQUARE_SIZE / 2)), PIECE_RADIUS)
    else:
        pygame.mouse.set_visible(True)


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
            if board[r][c] == EMPTY_CELL:
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


def alterButtonAppearance(button, color, outline):
    """
    Alter button appearance with given colors
    :param button:
    :param color:
    :param outline:
    :return:
    """
    button.color = color
    button.draw(outline)


def buttonResponseToMouseEvent(event):
    """
    Handles button behaviour in response to mouse events influencing them
    """
    if event.type == pygame.MOUSEMOTION:
        if showStatsButton.hover(event.pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            alterButtonAppearance(showStatsButton, WHITE, BLACK)
        elif contributorsButton.hover(event.pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            alterButtonAppearance(contributorsButton, WHITE, BLACK)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            alterButtonAppearance(showStatsButton, LIGHTGREY, BLACK)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if showStatsButton.hover(event.pos):
            alterButtonAppearance(showStatsButton, CYAN, BLACK)
        elif contributorsButton.hover(event.pos):
            alterButtonAppearance(contributorsButton, CYAN, BLACK)

    if event.type == pygame.MOUSEBUTTONUP:
        if showStatsButton.hover(event.pos):
            alterButtonAppearance(showStatsButton, LIGHTGREY, BLACK)
        elif contributorsButton.hover(event.pos):
            alterButtonAppearance(contributorsButton, LIGHTGREY, BLACK)
            showContributors()


def showContributors():
    """
    Invoked at pressing the contributors button. Displays a message box Containing names and IDs of contributors
    """
    messagebox.showinfo('Contributors', "6744   -   Adham Mohamed Aly\n"
                                        "6905   -   Mohamed Farid Abdelaziz\n"
                                        "7140   -   Yousef Ashraf Kotp\n")


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

            buttonResponseToMouseEvent(event)

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


def gradientRect(window, left_colour, right_colour, target_rect):
    """
    Draw a horizontal-gradient filled rectangle covering <target_rect>
    """
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))  # left colour line
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))  # right colour line
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)


if __name__ == '__main__':
    pygame.init()
    setupFrame()
    gameSession()
