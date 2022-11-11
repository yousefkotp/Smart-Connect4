import math
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog

import numpy as np
import pygame

import engine

win = tk.Tk()
win.withdraw()

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
DARKGREEN = (0, 190, 0)
BLUE = (30, 30, 122)
CYAN = (30, 230, 230)
GOLD = (225, 185, 0)
DARKGOLD = (165, 125, 0)

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
PLAYER_SCORE = [0, 0, 0]
GAME_BOARD = [[]]
usePruning = True
useTranspositionTable = False
screen = pygame.display.set_mode(WINDOW_SIZE)
GAME_MODE = -1
gameInSession = False

#   Game Modes  #
SINGLE_PLAYER = 1
TWO_PLAYERS = 2

# Developer Mode: facilitates debugging during GUI development
DEVMODE = False


class GameWindow:
    def switch(self):
        self.refreshGameWindow()
        self.gameSession()

    def setupGameWindow(self):
        """
        Initializes the all components in the frame
        """
        global GAME_BOARD
        GAME_BOARD = self.initGameBoard(EMPTY_CELL)
        pygame.display.set_caption('Smart Connect4 :)')
        self.refreshGameWindow()

    def refreshGameWindow(self):
        """
        Refreshes the screen and all the components
        """
        pygame.display.flip()
        refreshBackground()
        self.drawGameBoard()
        self.drawGameWindowButtons()
        self.drawGameWindowLabels()

    ######   Labels    ######

    def drawGameWindowLabels(self):
        """
        Draws all labels on the screen
        """
        titleFont = pygame.font.SysFont("Sans Serif", 40, False, True)
        mainLabel = titleFont.render("Smart Connect4", True, WHITE)
        screen.blit(mainLabel, (BOARD_LAYOUT_END_X + 20, 20))

        if not GAME_OVER:
            captionFont = pygame.font.SysFont("Arial", 15)
            player1ScoreCaption = captionFont.render("Player1", True, BLACK)
            player2ScoreCaption = captionFont.render("Player2", True, BLACK)
            screen.blit(player1ScoreCaption, (BOARD_LAYOUT_END_X + 48, 210))
            screen.blit(player2ScoreCaption, (BOARD_LAYOUT_END_X + 170, 210))

            if GAME_MODE == SINGLE_PLAYER:
                global statsPanelY
                depthFont = pygame.font.SysFont("Serif", math.ceil(23 - len(str(engine.BOARD.getDepth())) / 4))
                depthLabel = depthFont.render("k = " + str(engine.BOARD.getDepth()), True, BLACK)

                tempWidth = WIDTH - (BOARD_LAYOUT_END_X + 10)
                centerX = BOARD_LAYOUT_END_X + 10 + (tempWidth / 2 - depthLabel.get_width() / 2)
                screen.blit(depthLabel, (centerX, 294))
                statsPanelY = 320

                if usePruning:
                    depthFont = pygame.font.SysFont("Arial", 16)
                    depthLabel = depthFont.render("Using alpha-beta pruning", True, GOLD)
                    centerX = BOARD_LAYOUT_END_X + 10 + (tempWidth / 2 - depthLabel.get_width() / 2)
                    screen.blit(depthLabel, (centerX, 320))
                    statsPanelY += 20

                if useTranspositionTable:
                    depthFont = pygame.font.SysFont("Arial", 16)
                    depthLabel = depthFont.render("Using transposition table", True, DARKGREEN)
                    centerX = BOARD_LAYOUT_END_X + 10 + (tempWidth / 2 - depthLabel.get_width() / 2)
                    screen.blit(depthLabel, (centerX, statsPanelY))
                    statsPanelY += 20

        else:
            if PLAYER_SCORE[PLAYER1] == PLAYER_SCORE[PLAYER2]:
                verdict = 'DRAW :)'
            elif PLAYER_SCORE[PLAYER1] > PLAYER_SCORE[PLAYER2]:
                verdict = 'Player 1 Wins!'
            else:
                verdict = 'Player 2 Wins!'

            verdictFont = pygame.font.SysFont("Serif", 40)
            verdictLabel = verdictFont.render(verdict, True, GOLD)
            screen.blit(verdictLabel, (BOARD_BEGIN_X + BOARD_END_X / 3, BOARD_BEGIN_Y / 3))

        self.refreshScores()
        self.refreshStats()

    def refreshScores(self):
        """
        Refreshes the scoreboard
        """
        if GAME_OVER:
            scoreBoard_Y = BOARD_BEGIN_Y
        else:
            scoreBoard_Y = 120

        pygame.draw.rect(screen, BLACK, (BOARD_LAYOUT_END_X + 9, scoreBoard_Y - 1, 117, 82), 0)
        player1ScoreSlot = pygame.draw.rect(screen, BOARD_LAYOUT_BACKGROUND,
                                            (BOARD_LAYOUT_END_X + 10, scoreBoard_Y, 115, 80))

        pygame.draw.rect(screen, BLACK, (BOARD_LAYOUT_END_X + 134, scoreBoard_Y - 1, 117, 82), 0)
        player2ScoreSlot = pygame.draw.rect(screen, BOARD_LAYOUT_BACKGROUND,
                                            (BOARD_LAYOUT_END_X + 135, scoreBoard_Y, 115, 80))

        scoreFont = pygame.font.SysFont("Sans Serif", 80)
        player1ScoreCounter = scoreFont.render(str(PLAYER_SCORE[PLAYER1]), True, PIECE_COLORS[1])
        player2ScoreCounter = scoreFont.render(str(PLAYER_SCORE[PLAYER2]), True, PIECE_COLORS[2])

        player1ScoreLength = player2ScoreLength = 2.7
        if PLAYER_SCORE[PLAYER1] > 0:
            player1ScoreLength += math.log(PLAYER_SCORE[PLAYER1], 10)
        if PLAYER_SCORE[PLAYER2] > 0:
            player2ScoreLength += math.log(PLAYER_SCORE[PLAYER2], 10)

        screen.blit(player1ScoreCounter,
                    (player1ScoreSlot.x + player1ScoreSlot.width / player1ScoreLength, scoreBoard_Y + 15))
        screen.blit(player2ScoreCounter,
                    (player2ScoreSlot.x + player2ScoreSlot.width / player2ScoreLength, scoreBoard_Y + 15))

    def mouseOverMainLabel(self):
        return 20 <= pygame.mouse.get_pos()[1] <= 45 and 810 <= pygame.mouse.get_pos()[0] <= 1030

    def refreshStats(self):
        """
        Refreshes the analysis section
        """
        if GAME_MODE == SINGLE_PLAYER:
            pygame.draw.rect(
                screen, BLACK,
                (BOARD_LAYOUT_END_X + 9, statsPanelY + 5, WIDTH - BOARD_LAYOUT_END_X - 18, 267 + (370 - statsPanelY)),
                0)
            pygame.draw.rect(
                screen, GREY,
                (BOARD_LAYOUT_END_X + 10, statsPanelY + 6, WIDTH - BOARD_LAYOUT_END_X - 20, 265 + (370 - statsPanelY)))

    ######   Buttons    ######

    def drawGameWindowButtons(self):
        """
            Draws all buttons on the screen
            """
        global showStatsButton, contributorsButton, \
            playAgainButton, settingsButton, homeButton
        global settingsIcon, settingsIconAccent, homeIcon, homeIconAccent

        settingsIcon = pygame.image.load('GUI/settings-icon.png').convert_alpha()
        settingsIconAccent = pygame.image.load('GUI/settings-icon-accent.png').convert_alpha()
        homeIcon = pygame.image.load('GUI/home-icon.png').convert_alpha()
        homeIconAccent = pygame.image.load('GUI/home-icon-accent.png').convert_alpha()

        contributorsButton = Button(
            screen, color=LIGHTGREY,
            x=BOARD_LAYOUT_END_X + 10, y=650,
            width=WIDTH - BOARD_LAYOUT_END_X - 20, height=30, text="Contributors")
        contributorsButton.draw(BLACK)

        if not GAME_OVER:
            settingsButton = Button(window=screen, color=(82, 82, 82), x=WIDTH - 48, y=BOARD_BEGIN_Y - 38,
                                    width=35, height=35)

            homeButton = Button(window=screen, color=(79, 79, 79), x=WIDTH - 88, y=BOARD_BEGIN_Y - 38,
                                width=35, height=35)
            self.reloadSettingsButton(settingsIcon)
            self.reloadHomeButton(homeIcon)

            showStatsButton_Y = 250
        else:
            showStatsButton_Y = 330

            playAgainButton = Button(
                window=screen, color=GOLD, x=BOARD_LAYOUT_END_X + 10, y=BOARD_BEGIN_Y + 100,
                width=WIDTH - BOARD_LAYOUT_END_X - 20, height=120, text="Play Again")
            playAgainButton.draw()

        if GAME_MODE == SINGLE_PLAYER:
            showStatsButton = Button(
                screen, color=LIGHTGREY,
                x=BOARD_LAYOUT_END_X + 10, y=showStatsButton_Y,
                width=WIDTH - BOARD_LAYOUT_END_X - 20, height=30, text="Show nerdy stats :D")
            showStatsButton.draw(BLACK)

    def reloadSettingsButton(self, icon):
        settingsButton.draw()
        screen.blit(icon, (settingsButton.x + 2, settingsButton.y + 2))

    def reloadHomeButton(self, icon):
        homeButton.draw()
        screen.blit(icon, (homeButton.x + 2, homeButton.y + 2))

    ######   Game Board  ######

    def initGameBoard(self, initialCellValue):
        """
        Initializes the game board with the value given.
        :param initialCellValue: Value of initial cell value
        :return: board list with all cells initialized to initialCellValue
        """
        global GAME_BOARD
        GAME_BOARD = np.full((ROW_COUNT, COLUMN_COUNT), initialCellValue)
        return GAME_BOARD

    def printGameBoard(self):
        """
        Prints the game board to the terminal
        """
        print('\n-\n' +
              str(GAME_BOARD) +
              '\n Player ' + str(TURN) + ' plays next')

    def drawGameBoard(self):
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
                piece = GAME_BOARD[r][c]
                pygame.draw.rect(
                    screen, CELL_BORDER_COLOR, (col, row, SQUARE_SIZE, SQUARE_SIZE))
                pygame.draw.circle(
                    screen, PIECE_COLORS[piece], (int(col + SQUARE_SIZE / 2), int(row + SQUARE_SIZE / 2)), PIECE_RADIUS)
        pygame.display.update()

    def hoverPieceOverSlot(self):
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

    def dropPiece(self, col, piece) -> tuple:
        """
        Drops the given piece in the next available cell in slot 'col'
        :param col: Column index where the piece will be dropped
        :param piece: Value of the piece to be put in array.
        :returns: tuple containing the row and column of piece position
        """
        row = self.getNextOpenRow(col)
        GAME_BOARD[row][col] = piece

        return row, col

    def hasEmptyCell(self, col) -> bool:
        """
        Checks if current slot has an empty cell. Assumes col is within array limits
        :param col: Column index representing the slot
        :return: True if slot has an empty cell. False otherwise.
        """
        return GAME_BOARD[0][col] == EMPTY_CELL

    def getNextOpenRow(self, col):
        """
        Gets the next available cell in the slot
        :param col: Column index
        :return: If exists, the row of the first available empty cell in the slot. None otherwise.
        """
        for r in range(ROW_COUNT - 1, -1, -1):
            if GAME_BOARD[r][col] == EMPTY_CELL:
                return r
        return None

    def boardIsFull(self) -> bool:
        """
        Checks if the board game is full
        :return: True if the board list has no empty slots, False otherwise.
        """
        for slot in range(COLUMN_COUNT):
            if self.hasEmptyCell(slot):
                return False
        return True

    def getBoardColumnFromPos(self, posx):
        """
        Get the index of the board column corresponding to the given position
        :param posx: Position in pixels
        :return: If within board bounds, the index of corresponding column, None otherwise
        """
        column = int(math.floor(posx / SQUARE_SIZE))
        if 0 <= column < COLUMN_COUNT:
            return column
        return None

    def buttonResponseToMouseEvent(self, event):
        """
        Handles button behaviour in response to mouse events influencing them
        """
        if event.type == pygame.MOUSEMOTION:
            if GAME_MODE == SINGLE_PLAYER and showStatsButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(showStatsButton, WHITE, BLACK)
            elif contributorsButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(contributorsButton, WHITE, BLACK)
            elif settingsButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.reloadSettingsButton(settingsIconAccent)
            elif homeButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.reloadHomeButton(homeIconAccent)
            elif GAME_OVER and playAgainButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(
                    button=playAgainButton, color=GOLD, outlineColor=BLACK, hasGradBackground=True,
                    gradLeftColor=WHITE, gradRightColor=GOLD, fontSize=22)
            elif self.mouseOverMainLabel():
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if GAME_MODE == SINGLE_PLAYER:
                    alterButtonAppearance(showStatsButton, LIGHTGREY, BLACK)
                alterButtonAppearance(contributorsButton, LIGHTGREY, BLACK)
                self.reloadSettingsButton(settingsIcon)
                self.reloadHomeButton(homeIcon)
                if GAME_OVER:
                    alterButtonAppearance(playAgainButton, GOLD, BLACK)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if GAME_MODE == SINGLE_PLAYER and showStatsButton.isOver(event.pos):
                alterButtonAppearance(showStatsButton, CYAN, BLACK)
            elif contributorsButton.isOver(event.pos):
                alterButtonAppearance(contributorsButton, CYAN, BLACK)
            elif GAME_OVER and playAgainButton.isOver(event.pos):
                alterButtonAppearance(
                    button=playAgainButton, color=GOLD, outlineColor=BLACK, hasGradBackground=True,
                    gradLeftColor=GOLD, gradRightColor=CYAN)
            elif self.mouseOverMainLabel() or homeButton.isOver(event.pos):
                self.resetEverything()
                mainMenu.setupMainMenu()
                mainMenu.show()
            elif settingsButton.isOver(event.pos):
                settingsWindow = SettingsWindow()
                settingsWindow.setupSettingsMenu()
                settingsWindow.show()

        if event.type == pygame.MOUSEBUTTONUP:
            if GAME_MODE == SINGLE_PLAYER and showStatsButton.isOver(event.pos):
                alterButtonAppearance(showStatsButton, LIGHTGREY, BLACK)
            elif contributorsButton.isOver(event.pos):
                alterButtonAppearance(contributorsButton, LIGHTGREY, BLACK)
                self.showContributors()
            elif GAME_OVER and playAgainButton.isOver(event.pos):
                alterButtonAppearance(
                    button=playAgainButton, color=GOLD, outlineColor=BLACK, hasGradBackground=True,
                    gradLeftColor=WHITE, gradRightColor=GOLD, fontSize=22)
                self.resetEverything()

        if DEVMODE:
            pygame.draw.rect(screen, BLACK, (BOARD_LAYOUT_END_X + 20, 70, WIDTH - BOARD_LAYOUT_END_X - 40, 40))
            pygame.mouse.set_visible(True)
            titleFont = pygame.font.SysFont("Sans Serif", 20, False, True)
            coordinates = titleFont.render(str(pygame.mouse.get_pos()), True, WHITE)
            screen.blit(coordinates, (BOARD_LAYOUT_END_X + 100, 80))

    def showContributors(self):
        """
        Invoked at pressing the contributors button. Displays a message box Containing names and IDs of contributors
        """
        messagebox.showinfo('Contributors', "6744   -   Adham Mohamed Aly\n"
                                            "6905   -   Mohamed Farid Abdelaziz\n"
                                            "7140   -   Yousef Ashraf Kotp\n")

    def gameSession(self):
        """
        Runs the game session
        """
        global GAME_OVER, TURN, GAME_BOARD, gameInSession
        gameInSession = True
        while True:
            if not GAME_OVER:
                self.hoverPieceOverSlot()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                self.buttonResponseToMouseEvent(event)

                if not GAME_OVER and event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0] - BOARD_BEGIN_X
                    column = self.getBoardColumnFromPos(posx)

                    if column is not None:
                        if self.hasEmptyCell(column):
                            self.dropPiece(column, TURN)
                            self.computeScore()
                            switchTurn()
                            self.refreshGameWindow()

                            self.player2Play()
                            if self.boardIsFull():
                                GAME_OVER = True
                                pygame.mouse.set_visible(True)
                                self.refreshGameWindow()
                                break
                            self.printGameBoard()

    def player2Play(self):
        if GAME_MODE == SINGLE_PLAYER:
            self.computerPlay()
        elif GAME_MODE == TWO_PLAYERS:
            pass

    def computerPlay(self):
        global GAME_BOARD
        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT):
                GAME_BOARD[i][j] -= 1

        flippedGameBoard = np.flip(m=GAME_BOARD, axis=0)  # Flip about x-axis
        numericState = engine.convertToNumber(flippedGameBoard)
        boardState = engine.nextMove(alphaBetaPruning=usePruning, state=numericState)
        flippedNewState = engine.convertToTwoDimensions(boardState)
        newState = np.flip(m=flippedNewState, axis=0)  # Flip about x-axis

        for i in range(ROW_COUNT):
            for j in range(COLUMN_COUNT):
                GAME_BOARD[i][j] += 1
                newState[i][j] += 1

        GAME_BOARD = newState
        self.computeScore()

        switchTurn()
        self.refreshGameWindow()

    def resetEverything(self):
        """
        Resets everything back to default values
        """
        global GAME_BOARD, PLAYER_SCORE, GAME_OVER, TURN
        PLAYER_SCORE = [0, 0, 0]
        GAME_OVER = False
        TURN = 1
        self.setupGameWindow()

    def computeScore(self):
        """
        Computes every player's score and stores it in the global PLAYER_SCORES list
        :returns: values in PLAYER_SCORES list
        """
        global PLAYER_SCORE
        PLAYER_SCORE = [0, 0, 0]
        for r in range(ROW_COUNT):
            consecutive = 0
            for c in range(COLUMN_COUNT):
                consecutive += 1
                if c > 0 and GAME_BOARD[r][c] != GAME_BOARD[r][c - 1]:
                    consecutive = 1
                if consecutive >= 4:
                    PLAYER_SCORE[GAME_BOARD[r][c]] += 1

        for c in range(COLUMN_COUNT):
            consecutive = 0
            for r in range(ROW_COUNT):
                consecutive += 1
                if r > 0 and GAME_BOARD[r][c] != GAME_BOARD[r - 1][c]:
                    consecutive = 1
                if consecutive >= 4:
                    PLAYER_SCORE[GAME_BOARD[r][c]] += 1

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                if GAME_BOARD[r][c] == GAME_BOARD[r + 1][c + 1] \
                        == GAME_BOARD[r + 2][c + 2] == GAME_BOARD[r + 3][c + 3]:
                    PLAYER_SCORE[GAME_BOARD[r][c]] += 1

        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 1, 2, -1):
                if GAME_BOARD[r][c] == GAME_BOARD[r + 1][c - 1] \
                        == GAME_BOARD[r + 2][c - 2] == GAME_BOARD[r + 3][c - 3]:
                    PLAYER_SCORE[GAME_BOARD[r][c]] += 1

        return PLAYER_SCORE

    def isWithinBounds(self, mat, r, c) -> bool:
        """
        :param mat: 2D matrix to check in
        :param r: current row
        :param c: current column
        :return: True if coordinates are within matrix bounds, False otherwise
        """
        return 0 <= r <= len(mat) and 0 <= c <= len(mat[0])


class MainMenu:
    def switch(self):
        self.setupMainMenu()
        self.show()

    def show(self):
        while GAME_MODE == -1:
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                self.buttonResponseToMouseEvent(event)

        startGameSession()

    def setupMainMenu(self):
        """
        Initializes the all components in the frame
        """
        global GAME_MODE, gameInSession
        GAME_MODE = -1
        gameInSession = False
        pygame.display.flip()
        pygame.display.set_caption('Smart Connect4 :) - Main Menu')
        self.refreshMainMenu()

    def refreshMainMenu(self):
        """
        Refreshes the screen and all the components
        """
        pygame.display.flip()
        refreshBackground(BLACK, GREY)
        self.drawMainMenuButtons()
        self.drawMainMenuLabels()

    def drawMainMenuButtons(self):
        global singlePlayerButton, multiPlayerButton, SettingsButton_MAINMENU
        singlePlayerButton = Button(
            window=screen, color=LIGHTGREY, x=WIDTH / 3, y=HEIGHT / 3, width=WIDTH / 3, height=HEIGHT / 6,
            gradCore=True, coreLeftColor=GREEN, coreRightColor=BLUE, text='PLAY AGAINST AI')

        multiPlayerButton = Button(
            window=screen, color=LIGHTGREY, x=WIDTH / 3, y=HEIGHT / 3 + HEIGHT / 5, width=WIDTH / 3,
            height=HEIGHT / 6,
            gradCore=True, coreLeftColor=GREEN, coreRightColor=BLUE, text='TWO-PLAYERS')

        SettingsButton_MAINMENU = Button(
            window=screen, color=LIGHTGREY, x=WIDTH / 3, y=HEIGHT / 3 + HEIGHT / 2.5, width=WIDTH / 3,
            height=HEIGHT / 6,
            gradCore=True, coreLeftColor=GREEN, coreRightColor=BLUE, text='GAME SETTINGS')

        singlePlayerButton.draw(BLACK, 2)
        multiPlayerButton.draw(BLACK, 2)
        SettingsButton_MAINMENU.draw(BLACK, 2)

    def drawMainMenuLabels(self):
        titleFont = pygame.font.SysFont("Sans Serif", 65, False, True)
        mainLabel = titleFont.render("Welcome to Smart Connect4 :)", True, WHITE)
        screen.blit(mainLabel, (WIDTH / 5, HEIGHT / 8))

    def buttonResponseToMouseEvent(self, event):
        """
        Handles button behaviour in response to mouse events influencing them
        """
        if event.type == pygame.MOUSEMOTION:
            if singlePlayerButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(singlePlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=WHITE, gradRightColor=BLUE)
            elif multiPlayerButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(multiPlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=WHITE, gradRightColor=BLUE)
            elif SettingsButton_MAINMENU.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(SettingsButton_MAINMENU, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=WHITE, gradRightColor=BLUE)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                alterButtonAppearance(singlePlayerButton, LIGHTGREY, BLACK,
                                      hasGradBackground=True, gradLeftColor=GREEN, gradRightColor=BLUE)
                alterButtonAppearance(multiPlayerButton, LIGHTGREY, BLACK,
                                      hasGradBackground=True, gradLeftColor=GREEN, gradRightColor=BLUE)
                alterButtonAppearance(SettingsButton_MAINMENU, LIGHTGREY, BLACK,
                                      hasGradBackground=True, gradLeftColor=GREEN, gradRightColor=BLUE)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if singlePlayerButton.isOver(event.pos):
                alterButtonAppearance(singlePlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=GOLD, gradRightColor=BLUE)
            elif multiPlayerButton.isOver(event.pos):
                alterButtonAppearance(multiPlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=GOLD, gradRightColor=BLUE)
            elif SettingsButton_MAINMENU.isOver(event.pos):
                alterButtonAppearance(SettingsButton_MAINMENU, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=GOLD, gradRightColor=BLUE)

        if event.type == pygame.MOUSEBUTTONUP:
            global GAME_MODE
            if singlePlayerButton.isOver(event.pos):
                alterButtonAppearance(singlePlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=GREEN, gradRightColor=BLUE)
                setGameMode(SINGLE_PLAYER)
            elif multiPlayerButton.isOver(event.pos):
                alterButtonAppearance(multiPlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=GREEN, gradRightColor=BLUE)
                setGameMode(TWO_PLAYERS)
            elif SettingsButton_MAINMENU.isOver(event.pos):
                alterButtonAppearance(multiPlayerButton, WHITE, BLACK,
                                      hasGradBackground=True, gradLeftColor=GREEN, gradRightColor=BLUE)
                settingsWindow = SettingsWindow()
                settingsWindow.switch()


class Button:
    def __init__(self, window, color, x, y, width, height, text='', isChecked=False, gradCore=False, coreLeftColor=None,
                 coreRightColor=None, gradOutline=False, outLeftColor=None, outRightColor=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.screen = window
        self.isChecked = isChecked
        self.gradCore = gradCore
        self.coreLeftColor = coreLeftColor
        self.coreRightColor = coreRightColor
        self.gradOutline = gradOutline
        self.outLeftColor = outLeftColor
        self.outRightColor = outRightColor

    def draw(self, outline=None, outlineThickness=2, font='comicsans', fontSize=15, fontColor=BLACK):
        """
        Draws the button on screen
        """
        if outline:
            rectOutline = pygame.draw.rect(self.screen, outline, (self.x, self.y,
                                                                  self.width, self.height), 0)
            if self.gradOutline:
                gradientRect(self.screen, self.outLeftColor, self.outRightColor, rectOutline)
        button = pygame.draw.rect(self.screen, self.color, (self.x + outlineThickness, self.y + outlineThickness,
                                                            self.width - 2 * outlineThickness,
                                                            self.height - 2 * outlineThickness), 0)
        if self.gradCore:
            gradientRect(self.screen, self.coreLeftColor, self.coreRightColor, button, self.text, font, fontSize)

        if self.text != '':
            font = pygame.font.SysFont(font, fontSize)
            text = font.render(self.text, True, fontColor)
            self.screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        return self, button

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False


class SettingsWindow:
    def switch(self):
        self.setupSettingsMenu()
        self.show()

    def show(self):
        while True:
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                self.buttonResponseToMouseEvent(event)

    def setupSettingsMenu(self):
        """
        Initializes the all components in the frame
        """
        pygame.display.flip()
        pygame.display.set_caption('Smart Connect4 :) - Game Settings')
        self.refreshSettingsMenu()

    def refreshSettingsMenu(self):
        """
        Refreshes the screen and all the components
        """
        pygame.display.flip()
        refreshBackground(BLACK, BLUE)
        self.drawSettingsMenuButtons()
        self.drawSettingsMenuLabels()

    def drawSettingsMenuButtons(self):
        global backButton, modifyDepthButton, pruningCheckbox, transpositionCheckbox, backIcon, backIconAccent

        backIconAccent = pygame.image.load('GUI/back-icon.png').convert_alpha()
        backIcon = pygame.image.load('GUI/back-icon-accent.png').convert_alpha()

        backButton = Button(window=screen, color=(26, 26, 120), x=WIDTH - 70, y=20, width=52, height=52)
        self.reloadBackButton(backIcon)


        pruningCheckbox = Button(
            screen, color=WHITE,
            x=30, y=320,
            width=30, height=30, text="",
            gradCore=usePruning, coreLeftColor=DARKGOLD, coreRightColor=GOLD,
            gradOutline=True, outLeftColor=LIGHTGREY, outRightColor=GREY)
        self.togglePruningCheckbox(toggle=False)

        transpositionCheckbox = Button(
            screen, color=WHITE,
            x=30, y=pruningCheckbox.y + pruningCheckbox.height + 20,
            width=30, height=30, text="",
            gradCore=useTranspositionTable, coreLeftColor=DARKGOLD, coreRightColor=GOLD,
            gradOutline=True, outLeftColor=LIGHTGREY, outRightColor=GREY)
        self.toggleTranspositionCheckbox(toggle=False)

        modifyDepthButton = Button(
            screen, color=LIGHTGREY,
            x=30, y=transpositionCheckbox.y + transpositionCheckbox.height + 20,
            width=200, height=50, text="Modify search depth k")
        modifyDepthButton.draw(BLACK)

    def reloadBackButton(self, icon):
        backButton.draw()
        screen.blit(icon, (backButton.x + 2, backButton.y + 2))

    def togglePruningCheckbox(self, toggle=True):
        global usePruning
        if toggle:
            usePruning = pruningCheckbox.isChecked = pruningCheckbox.gradCore = not usePruning

        if usePruning:
            pruningCheckbox.draw(WHITE, outlineThickness=4)
        else:
            pruningCheckbox.draw(WHITE, outlineThickness=2)

    def toggleTranspositionCheckbox(self, toggle=True):
        global usePruning, useTranspositionTable
        if toggle:
            useTranspositionTable = transpositionCheckbox.isChecked \
                = transpositionCheckbox.gradCore = not useTranspositionTable

        if useTranspositionTable:
            transpositionCheckbox.draw(WHITE, outlineThickness=4)
        else:
            transpositionCheckbox.draw(WHITE, outlineThickness=2)

    def drawSettingsMenuLabels(self):
        global aiSettingsHR

        titleFont = pygame.font.SysFont("Sans Serif", 65, False, True)
        subTitleFont = pygame.font.SysFont("Sans Serif", 50, False, True)
        captionFont1_Arial = pygame.font.SysFont("Arial", 16)
        captionFont1_SansSerif = pygame.font.SysFont("Sans Serif", 16)
        captionFont2_Arial = pygame.font.SysFont("Arial", 23)
        captionFont2_SansSerif = pygame.font.SysFont("Sans Serif", 23)

        mainLabel = titleFont.render("Game Settings", True, WHITE)
        aiSettingsSubtitle = subTitleFont.render("AI Settings", True, WHITE)
        pruningCaption = captionFont1_Arial.render("Use alpha-beta pruning", True, WHITE)
        transpositionCaption = captionFont1_Arial.render("Use transposition table", True, WHITE)
        depthCaption = captionFont2_Arial.render("k = " + str(engine.BOARD.getDepth()), True, WHITE)
        backLabel = captionFont2_SansSerif.render("BACK", True, WHITE)

        screen.blit(backLabel, (backButton.x + 5, backButton.y + backButton.height + 8))

        screen.blit(mainLabel, (WIDTH / 2 - mainLabel.get_width() / 2, HEIGHT / 8))

        screen.blit(aiSettingsSubtitle, (20, 250))
        aiSettingsHR = pygame.draw.rect(
            surface=screen,
            color=GREY,
            rect=(10, 250 + aiSettingsSubtitle.get_height() + 10, 600, 4))

        screen.blit(pruningCaption,
                    (pruningCheckbox.x + pruningCheckbox.width + 10,
                     pruningCheckbox.y + pruningCaption.get_height() / 3))

        screen.blit(transpositionCaption,
                    (transpositionCheckbox.x + transpositionCheckbox.width + 10,
                     transpositionCheckbox.y + transpositionCaption.get_height() / 3))

        screen.blit(depthCaption,
                    (modifyDepthButton.x + modifyDepthButton.width + 10,
                     modifyDepthButton.y + depthCaption.get_height() / 3))

    def buttonResponseToMouseEvent(self, event):
        """
        Handles button behaviour in response to mouse events influencing them
        """
        if event.type == pygame.MOUSEMOTION:
            if modifyDepthButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                alterButtonAppearance(modifyDepthButton, WHITE, BLACK, 4)
            elif pruningCheckbox.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif transpositionCheckbox.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            elif backButton.isOver(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.reloadBackButton(backIconAccent)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                alterButtonAppearance(modifyDepthButton, LIGHTGREY, BLACK)
                self.reloadBackButton(backIcon)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if modifyDepthButton.isOver(event.pos):
                alterButtonAppearance(modifyDepthButton, CYAN, BLACK)
            elif pruningCheckbox.isOver(event.pos):
                self.togglePruningCheckbox()
            elif transpositionCheckbox.isOver(event.pos):
                self.toggleTranspositionCheckbox()
            elif backButton.isOver(event.pos):
                if gameInSession:
                    gameWindow = GameWindow()
                    gameWindow.switch()
                else:
                    mainMenu.switch()

        elif event.type == pygame.MOUSEBUTTONUP:
            if modifyDepthButton.isOver(event.pos):
                alterButtonAppearance(modifyDepthButton, LIGHTGREY, BLACK)
                self.takeNewDepth()

    def takeNewDepth(self):
        """
        Invoked at pressing modify depth button. Displays a simple dialog that takes input depth from user
        """
        temp = simpledialog.askinteger('Enter depth', 'Enter depth k')
        if temp is not None and temp > 0:
            engine.BOARD.setDepth(temp)
        self.refreshSettingsMenu()


def gradientRect(window, left_colour, right_colour, target_rect, text=None, font='comicsans', fontSize=15):
    """
    Draw a horizontal-gradient filled rectangle covering <target_rect>
    """
    colour_rect = pygame.Surface((2, 2))  # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour, (0, 0), (0, 1))  # left colour line
    pygame.draw.line(colour_rect, right_colour, (1, 0), (1, 1))  # right colour line
    colour_rect = pygame.transform.smoothscale(colour_rect, (target_rect.width, target_rect.height))  # stretch!
    window.blit(colour_rect, target_rect)

    if text:
        font = pygame.font.SysFont(font, fontSize)
        text = font.render(text, True, (0, 0, 0))
        window.blit(text, (
            target_rect.x + (target_rect.width / 2 - text.get_width() / 2),
            target_rect.y + (target_rect.height / 2 - text.get_height() / 2)))


def alterButtonAppearance(button, color, outlineColor, outlineThickness=2,
                          hasGradBackground=False, gradLeftColor=None, gradRightColor=None, fontSize=15):
    """
    Alter button appearance with given colors
    """
    button.color = color
    thisButton, buttonRect = button.draw(outline=outlineColor, outlineThickness=outlineThickness)
    if hasGradBackground:
        gradientRect(screen, gradLeftColor, gradRightColor, buttonRect, thisButton.text, 'comicsans', fontSize)


def refreshBackground(leftColor=BLACK, rightColor=GREY):
    """
    Refreshes screen background
    """
    gradientRect(screen, leftColor, rightColor, pygame.draw.rect(screen, SCREEN_BACKGROUND, (0, 0, WIDTH, HEIGHT)))


def switchTurn():
    """
    Switch turns between player 1 and player 2
    """
    global TURN
    if TURN == 1:
        TURN = 2
    else:
        TURN = 1


def startGameSession():
    gameWindow = GameWindow()
    gameWindow.setupGameWindow()
    gameWindow.gameSession()


def setGameMode(mode):
    global GAME_MODE
    GAME_MODE = mode


if __name__ == '__main__':
    pygame.init()
    mainMenu = MainMenu()
    mainMenu.setupMainMenu()
    mainMenu.show()
