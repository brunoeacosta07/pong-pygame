import pygame_gui
from menus.menu import Menu
from utils.utils import *


def get_users():
    return open_csv('resources/files/maestro-usuarios.csv')


class UserRegs(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.id_x, self.name_x, self.user_x, self.pass_x, self.item_y = 110, 270, 630, 870, 150
        self.manager = pygame_gui.UIManager((self.game.DISPLAY_W, self.game.DISPLAY_H), "themes/theme.json")
        self.panel = pygame_gui.elements.ui_scrolling_container.UIScrollingContainer(
            relative_rect=pygame.Rect((20, 200), (self.game.DISPLAY_W - 100, self.game.DISPLAY_H - 200)),
            manager=self.manager,
            allow_scroll_x=False
        )
        self.users = []
        self.labels = []

    def update_panel(self):
        self.users = get_users()
        for i, user in enumerate(self.users):
            self.labels.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((0, i * 50), (self.panel.relative_rect.width / 4 - 40, 40)),
                text=user['codUsuario'],
                manager=self.manager,
                container=self.panel,
                object_id=f'#codUsuario_{i}',
            ))
            self.labels.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((self.panel.relative_rect.width / 4 + 20, i * 50),
                                          (self.panel.relative_rect.width / 4 - 20, 40)),
                text=user['nombreYApellido'],
                manager=self.manager,
                container=self.panel,
                object_id=f'#nombreYApellido_{i}',
            ))
            self.labels.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((self.panel.relative_rect.width / 2 + 60, i * 50),
                                          (self.panel.relative_rect.width / 4 - 60, 40)),
                text=user['usuario'],
                manager=self.manager,
                container=self.panel,
                object_id=f'#usuario_{i}',
            ))
            self.labels.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((3 * self.panel.relative_rect.width / 4 + 80, i * 50),
                                          (self.panel.relative_rect.width / 4 - 60, 40)),
                text=user['clave'],
                manager=self.manager,
                container=self.panel,
                object_id=f'#clave_{i}',
            ))

    async def display_menu(self):
        self.run_display = True
        self.update_panel()
        while self.run_display:
            await self.game.check_events()

            self.game.display.fill(BLACK)
            self.game.draw_title_text('Registro de usuarios', TITLE_TEXT_SIZE, self.game.DISPLAY_W / 2, 50)
            self.game.draw_text('ID', MENU_TEXT_SIZE - 20, self.id_x, self.item_y, GREEN)
            self.game.draw_text('Nombre y Apellido', MENU_TEXT_SIZE - 20, self.name_x, self.item_y, GREEN)
            self.game.draw_text('Usuario', MENU_TEXT_SIZE - 20, self.user_x, self.item_y, GREEN)
            self.game.draw_text('Contraseña', MENU_TEXT_SIZE - 20, self.pass_x, self.item_y, GREEN)
            self.manager.draw_ui(self.game.display)
            self.blit_screen()

    def check_input(self, event, time_delta):
        if self.game.START_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.reports
            self.run_display = False
        self.manager.update(time_delta)
