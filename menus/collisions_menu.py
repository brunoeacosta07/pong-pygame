import pygame_gui
from menus.menu import Menu
from utils.utils import *


def get_collisions(user):
    matches = open_csv('resources/files/detalle-colisiones.csv')
    return [match for match in matches if match['codUsuario'] == user['codUsuario']]


def get_matches(user):
    matches = open_csv('resources/files/detalle-partida-jugador.csv')
    return [match for match in matches if match['codUsuario'] == user['codUsuario']]


def get_users():
    return open_csv('resources/files/maestro-usuarios.csv')


def filter_unique_matches(matches):
    unique_matches = []
    for match in matches:
        if match['numPartida'] not in [um['numPartida'] for um in unique_matches]:
            unique_matches.append(match)
    return unique_matches


def get_collisions_details(user, target_match):
    collisions = get_collisions(user)
    return [collision for collision in collisions if collision['numPartida'] == target_match]


class CollisionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.user_dropdown_x, self.user_dropdown_y = 200, 150
        self.match_dropdown_x, self.match_dropdown_y = 450, 150
        self.search_button_x, self.search_button_y = 700, 150
        self.date_x, self.observation_x, self.collision_x = 160, 430, 830
        self.manager = pygame_gui.UIManager((self.game.DISPLAY_W, self.game.DISPLAY_H), "themes/theme-list.json")
        self.users = get_users()
        self.matches = []
        self.collisions_details = []
        self.labels = []
        self.error_message = None
        self.match_dropdown = None
        self.update_match_dropdown(self.users[0])
        self.user_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=[user['usuario'] for user in self.users],
            starting_option=self.users[0]['usuario'],
            relative_rect=pygame.Rect((self.user_dropdown_x, self.user_dropdown_y), (200, 50)),
            manager=self.manager,
            object_id='#user_dropdown'
        )
        self.submit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.search_button_x, self.search_button_y), (100, 50)),
            text='Buscar',
            manager=self.manager,
            object_id='#search_button'
        )
        self.panel = pygame_gui.elements.ui_scrolling_container.UIScrollingContainer(
            relative_rect=pygame.Rect((50, self.match_dropdown_y + 150), (self.game.DISPLAY_W-100,
                                                                          self.game.DISPLAY_H - 300)),
            manager=self.manager,
            allow_scroll_x=False
        )
        for i, detail in enumerate(self.collisions_details):
            self.labels.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, i * 50), (self.panel.relative_rect.width - 20, 40)),
                text=detail['fecha'],
                manager=self.manager,
                container=self.panel,
                object_id=f'#fecha_{i}',
            ))
            self.labels.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((100, i * 50), (self.panel.relative_rect.width - 20, 40)),
                text=detail['observacion'],
                manager=self.manager,
                container=self.panel,
                object_id=f'#observacion_{i}',
            ))
            self.labels.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((300, i * 50), (self.panel.relative_rect.width - 20, 40)),
                text=detail['colision'],
                manager=self.manager,
                container=self.panel,
                object_id=f'#colision_{i}',
            ))

    def update_match_dropdown(self, selected_user):
        self.matches = filter_unique_matches(get_matches(selected_user))
        if self.match_dropdown:
            self.match_dropdown.kill()

        self.match_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=[match['numPartida'] for match in self.matches],
            starting_option=self.matches[0]['numPartida'] if self.matches else '',
            relative_rect=pygame.Rect((self.match_dropdown_x, self.match_dropdown_y), (200, 50)),
            manager=self.manager,
            object_id='#match_dropdown'
        )

    def update_labels(self):
        for label in self.labels:
            label.kill()
        self.labels = []
        for i, detail in enumerate(self.collisions_details):
            self.labels.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((0, i * 50), (self.panel.relative_rect.width / 3 - 20, 40)),
                text=detail['fecha'],
                manager=self.manager,
                container=self.panel,
                object_id=f'#fecha_{i}',
            ))
            self.labels.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((self.panel.relative_rect.width / 3, i * 50),
                                          (self.panel.relative_rect.width / 3 - 20, 40)),
                text=detail['observacion'],
                manager=self.manager,
                container=self.panel,
                object_id=f'#observacion_{i}',
            ))
            self.labels.append(pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((2 * self.panel.relative_rect.width / 3, i * 50),
                                          (self.panel.relative_rect.width / 3 - 20, 40)),
                text=detail['colision'],
                manager=self.manager,
                container=self.panel,
                object_id=f'#colision_{i}',
            ))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.display.fill(BLACK)
            self.game.check_events()
            self.game.draw_title_text('Detalle de colisiones', TITLE_TEXT_SIZE, self.game.DISPLAY_W / 2, 50)
            self.game.draw_text('Usuario:', MENU_TEXT_SIZE - 20, self.user_dropdown_x, self.user_dropdown_y - 40)
            self.game.draw_text('Partida:', MENU_TEXT_SIZE - 20, self.match_dropdown_x, self.match_dropdown_y - 40)
            self.game.draw_text('Fecha', MENU_TEXT_SIZE - 20, self.date_x, self.match_dropdown_y + 100, GREEN)
            self.game.draw_text('PALETA|PELOTA', MENU_TEXT_SIZE - 20, self.observation_x, self.match_dropdown_y + 100, GREEN)
            self.game.draw_text('Detalle', MENU_TEXT_SIZE - 20, self.collision_x, self.match_dropdown_y + 100, GREEN)
            self.manager.draw_ui(self.game.display)

            if self.error_message:
                self.game.draw_text(self.error_message, 24, self.user_dropdown_x, self.match_dropdown_y + 55, RED)
            self.blit_screen()

    def check_input(self, event, time_delta):
        if self.game.START_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.reports
            self.run_display = False
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.user_dropdown:
            selected_user_name = event.text
            selected_user = next(user for user in self.users if user['usuario'] == selected_user_name)
            self.update_match_dropdown(selected_user)
            if not self.matches:
                self.error_message = '*No se encontraron partidas para el usuario seleccionado*'
                self.collisions_details = []
                self.labels = []
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.submit_button:
                selected_match = self.match_dropdown.selected_option[0]
                selected_user_name = self.user_dropdown.selected_option[0]
                selected_user = next(user for user in self.users if user['usuario'] == selected_user_name)
                self.collisions_details = get_collisions_details(selected_user, selected_match)
                self.update_labels()
                self.error_message = None
                if not self.collisions_details:
                    self.error_message = '*No se encontraron detalles para la partida seleccionada*'
        self.manager.update(time_delta)
