from menus.menu import Menu
from utils.utils import *


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    async def display_menu(self):
        self.run_display = True
        while self.run_display:
            await self.game.check_events()
            if self.game.START_KEY or self.game.ESCAPE_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(BLACK)
            self.game.draw_title_text('Creditos', TITLE_TEXT_SIZE, self.mid_w, self.game.DISPLAY_H / 3)
            self.game.draw_text('- Acosta Bruno', MENU_TEXT_SIZE, OPTIONS_TEXT_POS, menu_text_height(self.mid_h, 1))
            self.game.draw_text('- Urizar Bryan', MENU_TEXT_SIZE, OPTIONS_TEXT_POS, menu_text_height(self.mid_h, 2))
            self.blit_screen()
