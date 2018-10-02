# Pygame and system modules
import sys
import pygame
from pygame.locals import *
from . import window

# Initializes pygame's modules
pygame.init()
pygame.font.init()


class Font():
    def __init__(self, text, font_family="ubuntu", size=10, color=(0, 0, 0), aa=False, local_font=False):
        if local_font:
            self.font = pygame.font.Font(font_family, size)
        else:
            self.font = pygame.font.SysFont(font_family, size)
        self.text = text
        self.surface = self.font.render(text, aa, color)
        self.color = color
        self.aa = aa  # Anti-aliasing

        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

        self.x = 0
        self.y = 0

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def change_text(self, text):
        self.text = text
        self.surface = self.font.render(text, self.aa, self.color)

        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

    def draw(self):
        window.Window.get_screen().blit(self.surface, (self.x, self.y))
