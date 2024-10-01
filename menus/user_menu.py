from menus.load_match import LoadMatchMenu
from menus.menu import Menu
from menus.personal_ranking import PersonalRanking
from utils.utils import *


class UserMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = NEW_GAME
        x_pos = OPTIONS_TEXT_POS + 100
        self.new_game_x, self.new_game_y = x_pos, menu_text_height(self.mid_h, 1)
        self.load_game_x, self.load_game_y = x_pos, menu_text_height(self.mid_h, 2)
        self.ranking_x, self.ranking_y = x_pos, menu_text_height(self.mid_h, 3)
        self.logout_x, self.logout_y = x_pos, menu_text_height(self.mid_h, 4)
        self.cursor_rect.midtop = (self.new_game_x + self.offset, self.new_game_y)
        self.user = None
        self.loadMenu = LoadMatchMenu(game)
        self.rankingMenu = PersonalRanking(game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(BLACK)
            if self.user:
                self.game.draw_title_text(f'Bienvenido {self.user['usuario']}',
                                          TITLE_TEXT_SIZE, self.mid_w, self.mid_h / 2)
            self.game.draw_text("Nueva Partida", MENU_TEXT_SIZE, self.new_game_x, self.new_game_y)
            self.game.draw_text("Cargar Partida", MENU_TEXT_SIZE, self.load_game_x, self.load_game_y)
            self.game.draw_text("Ranking Personal", MENU_TEXT_SIZE, self.ranking_x, self.ranking_y)
            self.game.draw_text("Cerrar Sesión", MENU_TEXT_SIZE, self.logout_x, self.logout_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == NEW_GAME:
                self.cursor_rect.midtop = (self.load_game_x + self.offset, self.load_game_y)
                self.state = LOAD_GAME
            elif self.state == LOAD_GAME:
                self.cursor_rect.midtop = (self.ranking_x + self.offset, self.ranking_y)
                self.state = RANKING
            elif self.state == RANKING:
                self.cursor_rect.midtop = (self.logout_x + self.offset, self.logout_y)
                self.state = LOGOUT
            elif self.state == LOGOUT:
                self.cursor_rect.midtop = (self.new_game_x + self.offset, self.new_game_y)
                self.state = NEW_GAME
        elif self.game.UP_KEY:
            if self.state == NEW_GAME:
                self.cursor_rect.midtop = (self.logout_x + self.offset, self.logout_y)
                self.state = LOGOUT
            elif self.state == LOAD_GAME:
                self.cursor_rect.midtop = (self.new_game_x + self.offset, self.new_game_y)
                self.state = NEW_GAME
            elif self.state == RANKING:
                self.cursor_rect.midtop = (self.load_game_x + self.offset, self.load_game_y)
                self.state = LOAD_GAME
            elif self.state == LOGOUT:
                self.cursor_rect.midtop = (self.ranking_x + self.offset, self.ranking_y)
                self.state = RANKING

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == NEW_GAME:
                self.game.curr_menu = self.game.main_menu
                matches = open_csv('resources/files/acumulador-partidas.csv')
                self.game.match_number = (int(matches[-1]['acumPartida']) + 1) if matches else 1
                self.run_display = False
                self.game.playing = True
            elif self.state == LOAD_GAME:
                self.game.curr_menu = self.loadMenu
            elif self.state == RANKING:
                self.game.curr_menu = self.rankingMenu
            elif self.state == LOGOUT:
                self.game.curr_menu = self.game.main_menu
                self.user = None
                self.cursor_rect.midtop = (self.new_game_x + self.offset, self.new_game_y)
                self.state = NEW_GAME
                self.run_display = False
            self.run_display = False

    def get_user_data(self, username):
        user_list = open_csv('resources/files/maestro-usuarios.csv')
        for user in user_list:
            if user['usuario'] == username:
                self.user = user
                break
