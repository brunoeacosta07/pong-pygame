import pygame_gui
from menus.menu import Menu
from utils.utils import *
from collections import defaultdict


def get_ranking_data():
    users_data = defaultdict(lambda: {'points': 0, 'games': set()})
    users = open_csv('resources/files/detalle-partida-jugador.csv')
    user_master = open_csv('resources/files/maestro-usuarios.csv')
    for user in users:
        cod_user = user['codUsuario']
        name = next((u['usuario'] for u in user_master if u['codUsuario'] == cod_user), 'Desconocido')
        points = int(user['puntajeA'])
        match_num = user['numPartida']
        users_data[name]['points'] += points
        users_data[name]['games'].add(match_num)

    ranking = [
        (name, data['points'], len(data['games']))
        for name, data in users_data.items()
    ]
    ranking.sort(key=lambda x: x[1], reverse=True)

    result = [f"{i + 1}.{name} ({puntaje} puntos en {partidas} partidas)"
              for i, (name, puntaje, partidas) in enumerate(ranking)] if ranking else ["No hay partidas aun :("]
    return result


class RankingMenu(Menu):
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
        self.rankings = get_ranking_data()

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

    async def display_menu(self):
        self.update_rankings()
        self.run_display = True
        while self.run_display:
            await self.game.check_events()

            self.game.display.fill(BLACK)
            self.game.draw_title_text('Ranking', TITLE_TEXT_SIZE, self.game.DISPLAY_W / 2, 50)
            self.manager.draw_ui(self.game.display)
            self.blit_screen()

    def check_input(self, event, time_delta):
        if self.game.START_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.reports
            self.run_display = False
        self.manager.update(time_delta)
