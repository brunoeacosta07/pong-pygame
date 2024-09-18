import sys

import pygame
from pygame.locals import *
import utils.utils as utils
from utils.utils import WIDTH, HEIGHT, WHITE
from sprites.ball import Ball
from sprites.paddle import Paddle
from sprites.text import Text

if not pygame.font:
    print('Warning, fonts disabled')


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Test")
    background_image = utils.load_image('img/background_tenis.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    ball = Ball()
    ball2 = Ball()
    ball3 = Ball()
    clock = pygame.time.Clock()
    player_paddle = Paddle(30)
    player_paddle.speed += 0.2
    cpu_paddle = Paddle(WIDTH-30)
    text = Text()
    scores = [0, 0]

    while True:
        time = clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
        ball.update(time, player_paddle, cpu_paddle, scores)
        ball2.update(time + 10, player_paddle, cpu_paddle, scores)
        ball3.update(time + 20, player_paddle, cpu_paddle, scores)
        player_paddle.move(time, keys)
        cpu_paddle.ai(time, ball)
        screen.blit(background_image, (0, 0))
        text.render(screen, f"P1: {scores[1]}", WHITE, (20, 10))
        text.render(screen, f"CPU: {scores[0]}", WHITE, (WIDTH-85, 10))
        screen.blit(ball.image, ball.rect)
        screen.blit(ball2.image, ball2.rect)
        screen.blit(ball3.image, ball3.rect)
        screen.blit(player_paddle.image, player_paddle.rect)
        screen.blit(cpu_paddle.image, cpu_paddle.rect)
        pygame.display.flip()


if __name__ == '__main__':
    main()
