import pygame
from pygame.locals import *
import sys

import utils.utils as utils
from utils.utils import WIDTH, HEIGHT, SPEED


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = utils.load_image("resources/img/paddle.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width(), 160))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = HEIGHT / 2
        self.speed = SPEED+0.1
        self.target_ball = None

    def move(self, time, keys):
        if keys[K_q]:
            pygame.quit()
            sys.exit(0)
        if (keys[K_UP] or keys[K_w]) and self.rect.top >= 0:
            self.rect.centery -= self.speed * time
        if (keys[K_DOWN] or keys[K_s]) and self.rect.bottom <= HEIGHT:
            self.rect.centery += self.speed * time

    def ai(self, time):
        if self.target_ball:
            if self.rect.colliderect(self.target_ball.rect):
                self.update_target_ball([self.target_ball])
            elif self.target_ball.rect.centerx > WIDTH / 2:
                if self.rect.top > 0 or self.rect.bottom < HEIGHT:
                    target_y = self.target_ball.rect.centery
                    self.rect.centery += (target_y - self.rect.centery) * 0.1 * time

    def update_target_ball(self, balls):
        if not self.target_ball or self.rect.colliderect(self.target_ball.rect):

            if self.target_ball:
                balls = [ball for ball in balls if ball.number != self.target_ball.number]
            if balls:
                self.target_ball = min(balls, key=lambda ball: abs(self.rect.centery - ball.rect.centery))
