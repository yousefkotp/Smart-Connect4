import pygame

from interface import gradientRect


class Button:
    def __init__(self, screen, color, x, y, width, height, text='', isChecked=False, gradCore=False, coreLeftColor=None,
                 coreRightColor=None, gradOutline=False, outLeftColor=None, outRightColor=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.screen = screen
        self.isChecked = isChecked
        self.gradCore = gradCore
        self.coreLeftColor = coreLeftColor
        self.coreRightColor = coreRightColor
        self.gradOutline = gradOutline
        self.outLeftColor = outLeftColor
        self.outRightColor = outRightColor

    def draw(self, outline=None, outlineThickness=2, font='comicsans', fontSize=15, ):
        """
        Draws the button on screen
        :param outline: Outline color
        :param font: Font Name
        :param fontSize: Font Size
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
            text = font.render(self.text, True, (0, 0, 0))
            self.screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        return self, button

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False
