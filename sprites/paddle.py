import pygame
from pygame.locals import *
import sys

import utils.utils as utils
from utils.utils import WIDTH, HEIGHT, SPEED


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = utils.load_image("img/paddle.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = SPEED+0.1

    def move(self, time, keys):
        if keys[K_q]:
            pygame.quit()
            sys.exit(0)
        if (keys[K_UP] or keys[K_w]) and self.rect.top >= 0:
            self.rect.centery -= self.speed * time
        if (keys[K_DOWN] or keys[K_s]) and self.rect.bottom <= HEIGHT:
            self.rect.centery += self.speed * time

    def ai(self, time, ball):
        if ball.speed[0] >= 0 and ball.rect.centerx >= WIDTH / 2:
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += self.speed * time
            elif self.rect.centery > ball.rect.centery:
                self.rect.centery -= self.speed * time
        else:
            if self.rect.centery < HEIGHT / 2:
                self.rect.centery += self.speed * time
            elif self.rect.centery > HEIGHT / 2:
                self.rect.centery -= self.speed * time
            else:
                pass

