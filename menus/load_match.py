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


class LoadMatchMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.matches_dropdown_x, self.matches_dropdown_y = 200, 150
        self.search_button_x, self.search_button_y = 400, 150
        self.points_a, self.points_b, self.date = 200, 450, 700
        self.manager = pygame_gui.UIManager((self.game.DISPLAY_W, self.game.DISPLAY_H), "themes/theme.json")
        self.matches = []
        self.match_detail = []
        self.labels = []
        self.error_message = None
        self.matches_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=[],
            starting_option='',
            relative_rect=pygame.Rect((self.matches_dropdown_x, self.matches_dropdown_y), (200, 50)),
            manager=self.manager,
            object_id='#matches_dropdown'
        )
        self.submit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.search_button_x, self.search_button_y), (150, 50)),
            text='Retomar partida',
            manager=self.manager,
            object_id='#search_button'
        )

    def update_match_detail(self, selected_match):
        self.match_detail = get_match_details(self.matches, selected_match)

    async def display_menu(self):
        self.run_display = True
        self.matches = get_matches(self.game.user_menu.user)
        if self.matches and len(self.matches) > 0:
            self.update_match_detail(self.matches[0]['numPartida'])
            self.matches_dropdown.kill()
            self.matches_dropdown = pygame_gui.elements.UIDropDownMenu(
                options_list=[match['numPartida'] for match in self.matches],
                starting_option=self.matches[0]['numPartida'],
                relative_rect=pygame.Rect((self.matches_dropdown_x, self.matches_dropdown_y), (200, 50)),
                manager=self.manager,
                object_id='#matches_dropdown'
            )
        else:
            self.submit_button.kill()
            self.submit_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.search_button_x, self.search_button_y), (150, 50)),
                text='Nuevo Juego',
                manager=self.manager,
                object_id='#search_button'
            )
            self.error_message = '*No existen partidas para este usuario*'

        while self.run_display:
            await self.game.check_events()
            self.game.display.fill(BLACK)
            self.game.draw_title_text(f"Cargar partida ({self.game.user_menu.user['usuario']})", TITLE_TEXT_SIZE,
                                      self.game.DISPLAY_W / 2, 50)
            self.game.draw_text('Partida:', MENU_TEXT_SIZE - 20, self.matches_dropdown_x, self.matches_dropdown_y - 40)
            self.game.draw_text('Puntaje A', MENU_TEXT_SIZE - 20, self.points_a, self.matches_dropdown_y + 100)
            self.game.draw_text('Puntaje B', MENU_TEXT_SIZE - 20, self.points_b, self.matches_dropdown_y + 100)
            self.game.draw_text('Fecha', MENU_TEXT_SIZE - 20, self.date, self.matches_dropdown_y + 100)
            if self.error_message:
                self.game.draw_text(self.error_message, 24, self.matches_dropdown_x, self.matches_dropdown_y + 55, RED)
            if self.match_detail:
                self.game.draw_text(f"{self.match_detail['puntajeA']}", MENU_TEXT_SIZE - 20, self.points_a,
                                    self.matches_dropdown_y + 150, GREEN)
                self.game.draw_text(f"{self.match_detail['puntajeB']}", MENU_TEXT_SIZE - 20, self.points_b,
                                    self.matches_dropdown_y + 150, GREEN)
                self.game.draw_text(f"{self.match_detail['fechaPartida']}", MENU_TEXT_SIZE - 20, self.date,
                                    self.matches_dropdown_y + 150, GREEN)
            self.manager.draw_ui(self.game.display)

            self.blit_screen()

    def check_input(self, event, time_delta):
        if self.game.START_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.user_menu
            self.run_display = False
            self.match_detail = []
            self.matches = []
            self.matches_dropdown.clear()
            self.error_message = None
            self.submit_button.kill()
            self.submit_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.search_button_x, self.search_button_y), (150, 50)),
                text='Retomar partida',
                manager=self.manager,
                object_id='#search_button'
            )
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == self.matches_dropdown:
            selected_match = event.text
            self.update_match_detail(selected_match)
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.submit_button:
                if self.submit_button.text == 'Nuevo Juego':
                    matches = open_csv('resources/files/acumulador-partidas.csv')
                    self.game.match_number = int(matches[-1]['acumPartida']) + 1 if matches else 1
                else:
                    self.game.match_number = int(self.match_detail['numPartida'])
                    self.game.scores = [int(self.match_detail['puntajeA']), int(self.match_detail['puntajeB'])]
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
                self.game.playing = True
        self.manager.update(time_delta)
