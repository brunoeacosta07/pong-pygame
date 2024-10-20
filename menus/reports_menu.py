from menus.collisions_menu import CollisionsMenu
from menus.menu import Menu
from menus.ranking_menu import RankingMenu
from menus.user_query import UserQuery
from menus.user_regs import UserRegs
from utils.utils import *


class ReportsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = USER_REGS
        self.user_regs_x, self.user_regs_y = OPTIONS_TEXT_POS, menu_text_height(self.mid_h, 1)
        self.user_query_x, self.user_query_y = OPTIONS_TEXT_POS, menu_text_height(self.mid_h, 2)
        self.ranking_x, self.ranking_y = OPTIONS_TEXT_POS, menu_text_height(self.mid_h, 3)
        self.collisions_x, self.collisions_y = OPTIONS_TEXT_POS, menu_text_height(self.mid_h, 4)
        self.cursor_rect.midtop = (self.user_regs_x + self.offset, self.user_regs_y)
        self.user_regs = UserRegs(game)
        self.user_query = UserQuery(game)
        self.ranking = RankingMenu(game)
        self.collisions = CollisionsMenu(game)

    async def display_menu(self):
        self.run_display = True
        while self.run_display:
            await self.game.check_events()
            self.check_input()
            self.game.display.fill(BLACK)
            self.game.draw_title_text('Informes Generales', TITLE_TEXT_SIZE, self.mid_w, self.mid_h / 2)
            self.game.draw_text("Registro de usuarios", MENU_TEXT_SIZE, self.user_regs_x, self.user_regs_y)
            self.game.draw_text("Consulta de usuario", MENU_TEXT_SIZE, self.user_query_x, self.user_query_y)
            self.game.draw_text("Ranking general", MENU_TEXT_SIZE, self.ranking_x, self.ranking_y)
            self.game.draw_text("Colisiones", MENU_TEXT_SIZE, self.collisions_x, self.collisions_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == USER_REGS:
                self.cursor_rect.midtop = (self.user_query_x + self.offset, self.user_query_y)
                self.state = USER_QUERY
            elif self.state == USER_QUERY:
                self.cursor_rect.midtop = (self.ranking_x + self.offset, self.ranking_y)
                self.state = RANKING
            elif self.state == RANKING:
                self.cursor_rect.midtop = (self.collisions_x + self.offset, self.collisions_y)
                self.state = COLLISIONS
            elif self.state == COLLISIONS:
                self.cursor_rect.midtop = (self.user_regs_x + self.offset, self.user_regs_y)
                self.state = USER_REGS
        elif self.game.UP_KEY:
            if self.state == USER_REGS:
                self.cursor_rect.midtop = (self.collisions_x + self.offset, self.collisions_y)
                self.state = COLLISIONS
            elif self.state == COLLISIONS:
                self.cursor_rect.midtop = (self.ranking_x + self.offset, self.ranking_y)
                self.state = RANKING
            elif self.state == RANKING:
                self.cursor_rect.midtop = (self.user_query_x + self.offset, self.user_query_y)
                self.state = USER_QUERY
            elif self.state == USER_QUERY:
                self.cursor_rect.midtop = (self.user_regs_x + self.offset, self.user_regs_y)
                self.state = USER_REGS

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        if self.game.START_KEY:
            if self.state == USER_REGS:
                self.game.curr_menu = self.user_regs
            elif self.state == USER_QUERY:
                self.game.curr_menu = self.user_query
            elif self.state == RANKING:
                self.game.curr_menu = self.ranking
            elif self.state == COLLISIONS:
                self.game.curr_menu = self.collisions
            self.run_display = False
