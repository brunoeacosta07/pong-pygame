import pygame
import utils.utils as utils
from utils.utils import WIDTH, HEIGHT, SPEED


class Ball(pygame.sprite.Sprite):
    def __init__(self, number, initial_x=WIDTH / 2, initial_y=HEIGHT / 2):
        super().__init__()
        self.image = utils.load_image("resources/img/ball-1.png", True)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = initial_x
        self.rect.centery = initial_y
        self.speed = [SPEED, -SPEED]
        self.angle = 0
        self.number = number

    def update(self, time, player_paddle, cpu_paddle, scores):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time

        if self.rect.left <= 0:
            scores[1] += 1
            self.reset_position()
            self.speed = [-SPEED, SPEED]
        elif self.rect.right >= WIDTH:
            scores[0] += 1
            self.reset_position()
            self.speed = [SPEED, -SPEED]

        if self.rect.centery <= 30 or self.rect.centery >= HEIGHT-30:
            self.speed[1] = -self.speed[1]
            if self.speed[1] == 0:
                self.speed[1] = SPEED

        if pygame.sprite.collide_rect(self, player_paddle) or pygame.sprite.collide_rect(self, cpu_paddle):
            self.speed[0] = -self.speed[0]

        self.angle += 3
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.move_ip(self.speed[0] * time, self.speed[1] * time)

        return scores

    def update_in_menu(self, time, text_rects, ball=None):
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
        elif self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]

        if self.rect.left < 0 or self.rect.top < 0:
            self.rect.centerx = 35
            self.rect.centery = 35

        if ball:
            if pygame.sprite.collide_rect(self, ball):
                self.speed[0] = -self.speed[0]
                self.speed[1] = -self.speed[1]

        for text_rect in text_rects:
            if self.rect.colliderect(text_rect):
                if text_rects[0] == text_rect:
                    if abs(self.rect.right - text_rect.left) < 10 or abs(self.rect.left - text_rect.right) < 10:
                        self.speed[0] = -self.speed[0]
                    if abs(self.rect.bottom - text_rect.top) < 10 or abs(self.rect.top - text_rect.bottom) < 10:
                        self.speed[1] = -self.speed[1]
                else:
                    if self.rect.right >= text_rect.left > self.rect.left:
                        self.speed[0] = -self.speed[0]
                    elif self.rect.left <= text_rect.right < self.rect.right:
                        self.speed[0] = -self.speed[0]
                    if self.rect.bottom >= text_rect.top > self.rect.top:
                        self.speed[1] = -self.speed[1]
                    elif self.rect.top <= text_rect.bottom < self.rect.bottom:
                        self.speed[1] = -self.speed[1]

        self.angle += 3
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.move_ip(self.speed[0] * time, self.speed[1] * time)

    def reset_position(self):
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2

    def set_speed(self, speed):
        self.speed = [speed, -speed]
