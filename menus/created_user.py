from menus.menu import Menu
from utils.utils import *

class CreatedUser(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)


def display_menu(self):
    self.run_display = True

    while self.run_display:
        self.game.check_events()
        self.check_input()
        self.game.display.fill(BLACK)
        self.game.draw_title_text('Usuario creado con exito!', TITLE_TEXT_SIZE + 100, self.mid_w, self.mid_h)
        self.blit_screen()


def check_input(self):
    if self.game.ESCAPE_KEY or self.game.START_KEY:
        self.game.curr_menu = self.game.main_menu
        self.run_display = False