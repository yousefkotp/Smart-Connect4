import pygame


class Button:
    def __init__(self, screen, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.screen = screen

    def draw(self, outline=None, font='comicsans', fontSize=15):
        """
        Draws the button on screen
        :param outline: Outline color
        :param font: Font Name
        :param fontSize: Font Size
        """
        if outline:
            pygame.draw.rect(self.screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        button = pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(font, fontSize)
            text = font.render(self.text, True, (0, 0, 0))
            self.screen.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        return self, button

    def hover(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True

        return False
