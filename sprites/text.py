import pygame


class Text:
    def __init__(self, font_name=None, font_size=30):
        pygame.font.init()
        self.font = pygame.font.Font(font_name, font_size)
        self.size = font_size

    def render(self, surface, text, color, pos):
        x, y = pos
        for line in text.split("r"):
            surface.blit(self.font.render(line, True, color), (x, y))
            y += self.size
