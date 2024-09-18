from menus.menu import Menu
from sprites.ball import Ball
from utils.utils import *


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = LOGIN
        self.login_x, self.login_y = OPTIONS_TEXT_POS, menu_text_height(self.mid_h, 1)
        self.signup_x, self.signup_y = OPTIONS_TEXT_POS, menu_text_height(self.mid_h, 2)
        self.ranking_x, self.ranking_y = OPTIONS_TEXT_POS, menu_text_height(self.mid_h, 3)
        self.credits_x, self.credits_y = OPTIONS_TEXT_POS, menu_text_height(self.mid_h, 4)
        self.cursor_rect.midtop = (self.login_x + self.offset, self.login_y)
        self.ball = Ball()
        self.ball2 = Ball(initial_x=50, initial_y=50)
        self.ball.set_speed(0.1)
        self.ball2.set_speed(0.1)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(BLACK)
            main_text_rect = self.game.draw_title_text('Pong en Pygame', TITLE_TEXT_SIZE, self.mid_w, self.mid_h / 2)
            login_text_rect = self.game.draw_text("Iniciar Sesion", MENU_TEXT_SIZE, self.login_x, self.login_y)
            signup_text_rect = self.game.draw_text("Crear usuario", MENU_TEXT_SIZE, self.signup_x, self.signup_y)
            ranking_text_rect = self.game.draw_text("Ranking", MENU_TEXT_SIZE, self.ranking_x, self.ranking_y)
            credits_text_rect = self.game.draw_text("Creditos", MENU_TEXT_SIZE, self.credits_x, self.credits_y)
            self.ball.update_in_menu(10, [main_text_rect, login_text_rect, signup_text_rect, ranking_text_rect,
                                          credits_text_rect])
            self.ball2.update_in_menu(10, [main_text_rect, login_text_rect, signup_text_rect, ranking_text_rect,
                                           credits_text_rect])
            self.game.display.blit(self.ball.image, self.ball.rect)
            self.game.display.blit(self.ball2.image, self.ball2.rect)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == LOGIN:
                self.cursor_rect.midtop = (self.signup_x + self.offset, self.signup_y)
                self.state = SIGNUP
            elif self.state == SIGNUP:
                self.cursor_rect.midtop = (self.ranking_x + self.offset, self.ranking_y)
                self.state = RANKING
            elif self.state == RANKING:
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = CREDITS
            elif self.state == CREDITS:
                self.cursor_rect.midtop = (self.login_x + self.offset, self.login_y)
                self.state = LOGIN
        elif self.game.UP_KEY:
            if self.state == LOGIN:
                self.cursor_rect.midtop = (self.credits_x + self.offset, self.credits_y)
                self.state = CREDITS
            elif self.state == CREDITS:
                self.cursor_rect.midtop = (self.ranking_x + self.offset, self.ranking_y)
                self.state = RANKING
            elif self.state == RANKING:
                self.cursor_rect.midtop = (self.signup_x + self.offset, self.signup_y)
                self.state = SIGNUP
            elif self.state == SIGNUP:
                self.cursor_rect.midtop = (self.login_x + self.offset, self.login_y)
                self.state = LOGIN

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == LOGIN:
                self.game.curr_menu = self.game.login
            elif self.state == SIGNUP:
                self.game.curr_menu = self.game.signUp
            elif self.state == RANKING:
                self.game.curr_menu = self.game.ranking
            elif self.state == CREDITS:
                self.game.curr_menu = self.game.credits
            self.run_display = False
