import pygame_gui
from menus.menu import Menu
from utils.utils import *


def get_users():
    return open_csv('resources/files/maestro-usuarios.csv')


def get_matches(user):
    matches = open_csv('resources/files/detalle-partida-jugador.csv')
    return [match for match in matches if match['codUsuario'] == user['codUsuario']]


def filter_unique_matches(matches):
    unique_matches = []
    for match in matches:
        if match['numPartida'] not in [um['numPartida'] for um in unique_matches]:
            unique_matches.append(match)
    return unique_matches


def get_match_details(matches, target_match):
    for match in matches:
        if match['numPartida'] == target_match:
            return match


class UserQuery(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.user_dropdown_x, self.user_dropdown_y = 200, 150
        self.match_dropdown_x, self.match_dropdown_y = 450, 150
        self.search_button_x, self.search_button_y = 700, 150
        self.points_a, self.points_b, self.date = 200, 450, 700
        self.manager = pygame_gui.UIManager((self.game.DISPLAY_W, self.game.DISPLAY_H), "themes/theme.json")
        self.users = get_users()
        self.matches = []
        self.match_detail = []
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

    async def display_menu(self):
        self.run_display = True
        while self.run_display:
            await self.game.check_events()
            self.game.display.fill(BLACK)
            self.game.draw_title_text('Consulta por usuario', TITLE_TEXT_SIZE, self.game.DISPLAY_W / 2, 50)
            self.game.draw_text('Usuario:', MENU_TEXT_SIZE - 20, self.user_dropdown_x, self.user_dropdown_y - 40)
            self.game.draw_text('Partida:', MENU_TEXT_SIZE - 20, self.match_dropdown_x, self.match_dropdown_y - 40)
            self.game.draw_text('Puntaje A', MENU_TEXT_SIZE - 20, self.points_a, self.match_dropdown_y + 100)
            self.game.draw_text('Puntaje B', MENU_TEXT_SIZE - 20, self.points_b, self.match_dropdown_y + 100)
            self.game.draw_text('Fecha', MENU_TEXT_SIZE - 20, self.date, self.match_dropdown_y + 100)
            if self.match_detail:
                if self.match_detail:
                    self.game.draw_text(f"{self.match_detail['puntajeA']}", MENU_TEXT_SIZE - 20, self.points_a,
                                        self.match_dropdown_y + 150, GREEN)
                    self.game.draw_text(f"{self.match_detail['puntajeB']}", MENU_TEXT_SIZE - 20, self.points_b,
                                        self.match_dropdown_y + 150, GREEN)
                    self.game.draw_text(f"{self.match_detail['fechaPartida']}", MENU_TEXT_SIZE - 20, self.date,
                                        self.match_dropdown_y + 150, GREEN)
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
                self.match_detail = []
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.submit_button:
                selected_match = self.match_dropdown.selected_option[0]
                self.match_detail = get_match_details(self.matches, selected_match)
                self.error_message = None
                if not self.match_detail:
                    self.error_message = '*No se encontraron detalles para la partida seleccionada*'
        self.manager.update(time_delta)
