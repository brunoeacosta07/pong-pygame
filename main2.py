from game import Game
from utils.utils import *

if not pygame.font:
    print('Warning, fonts disabled')


def main():
    pygame.init()
    pygame.font.init()
    display = pygame.Surface((WIDTH, HEIGHT))
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong en Pygame")
    game = Game(display, window)
    while game.running:
        game.curr_menu.display_menu()
        game.game_loop()


if __name__ == '__main__':
    main()
