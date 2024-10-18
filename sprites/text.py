import pygame
from utils.utils import WHITE

class Text:
    def __init__(self, font_name=None, font_size=40):
        pygame.font.init()
        self.font = pygame.font.Font(font_name, font_size)
        self.size = font_size

    def render(self, surface, text, color, pos):
        x, y = pos
        # for line in text.split("r"):
        #     surface.blit(self.font.render(line, True, color), (x, y))
        #     y += self.size
        surface.blit(self.font.render(text, True, color), (x, y))

    def blit_text(self, surface, text, x, y, color=WHITE):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.left = x
        text_rect.top = y
        surface.blit(text_surface, text_rect)
        return text_rect
