import pygame_gui
from menus.menu import Menu
from utils.utils import *


class RankingMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.manager = pygame_gui.UIManager((self.game.DISPLAY_W, self.game.DISPLAY_H), "themes/theme.json")
        self.panel = pygame_gui.elements.ui_scrolling_container.UIScrollingContainer(
            relative_rect=pygame.Rect((50, 100), (self.game.DISPLAY_W - 100, self.game.DISPLAY_H - 200)),
            manager=self.manager,
            allow_scroll_x=False
        )
        self.rankings = ["1. Player1", "2. Player2", "3. Player3", "4. Player4", "5. Player5",
                         "6. Player6", "7. Player7", "8. Player8", "9. Player9", "10. Player10",
                         "11. Player11", "12. Player12", "13. Player13", "14. Player14", "15. Player15",
                         "16. Player16", "17. Player17", "18. Player18", "19. Player19", "20. Player20",
                         "21. Player21", "22. Player22", "23. Player23", "24. Player24", "25. Player25",
                         "26. Player26", "27. Player27", "28. Player28", "29. Player29", "30. Player30",
                         "31. Player31", "32. Player32", "33. Player33", "34. Player34", "35. Player35",
                         "36. Player36", "37. Player37", "38. Player38", "39. Player39", "40. Player40"]
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
        self.run_display = True
        while self.run_display:
            self.game.check_events()

            self.game.display.fill(BLACK)
            self.game.draw_title_text('Ranking', TITLE_TEXT_SIZE, self.game.DISPLAY_W / 2, 50)
            self.manager.draw_ui(self.game.display)
            self.blit_screen()

    def check_input(self, event, time_delta):
        if self.game.START_KEY or self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        self.manager.update(time_delta)
