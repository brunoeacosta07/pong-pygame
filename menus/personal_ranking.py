import pygame_gui
from menus.menu import Menu
from utils.utils import *
from collections import defaultdict


def get_ranking_data(user_data):
    users_data = defaultdict(lambda: {'point_a': 0, 'point_b': 0, 'total': set()})
    users = open_csv('resources/files/detalle-partida-jugador.csv')
    users = [user for user in users if user['codUsuario'] == user_data['codUsuario']]
    for user in users:
        point_a = int(user['puntajeA'])
        point_b = int(user['puntajeB'])
        match_num = user['numPartida']
        users_data[match_num]['point_a'] = point_a
        users_data[match_num]['point_b'] = point_b
        users_data[match_num]['total'] = point_a - point_b

    ranking = [
        (match_num, data['point_a'], data['point_b'], data['total'])
        for match_num, data in users_data.items()
    ]
    ranking.sort(key=lambda x: x[3], reverse=True)

    result = [f"{i + 1}. Partida: {match_num} | Puntos A: {puntaje_a} | Puntos B: {puntaje_b} | TOTAL: {total})"
              for i, (match_num, puntaje_a, puntaje_b, total)
              in enumerate(ranking)] if ranking else ["No hay partidas aun :("]
    return result


class PersonalRanking(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.manager = pygame_gui.UIManager((self.game.DISPLAY_W, self.game.DISPLAY_H), "themes/theme.json")
        self.panel = pygame_gui.elements.ui_scrolling_container.UIScrollingContainer(
            relative_rect=pygame.Rect((50, 100), (self.game.DISPLAY_W - 100, self.game.DISPLAY_H - 200)),
            manager=self.manager,
            allow_scroll_x=False
        )
        self.rankings = []
        self.labels = []

    def update_rankings(self):
        self.rankings = get_ranking_data(self.game.user_menu.user)

        self.labels = []
        for i, ranking in enumerate(self.rankings):
            label = pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((10, i * 50), (self.panel.relative_rect.width - 20, 40)),
                text=ranking,
                manager=self.manager,
                container=self.panel,
                object_id=f'#ranking_{i}',
            )
            self.labels.append(label)

    def display_menu(self):
        self.update_rankings()
        self.run_display = True
        while self.run_display:
            self.game.check_events()

            self.game.display.fill(BLACK)
            self.game.draw_title_text('Ranking Personal', TITLE_TEXT_SIZE, self.game.DISPLAY_W / 2, 50)
            self.manager.draw_ui(self.game.display)
            self.blit_screen()

    def check_input(self, event, time_delta):
        if self.game.START_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.user_menu
            self.run_display = False
        self.manager.update(time_delta)
