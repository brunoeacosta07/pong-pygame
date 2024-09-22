from menus.created_user import CreatedUser
from menus.credits_menu import CreditsMenu
from menus.login_menu import LoginMenu
from menus.main_menu import MainMenu
from menus.ranking_menu import RankingMenu
from menus.signup_menu import SignUpMenu
from menus.user_menu import UserMenu
from utils.utils import *
import sys


class Game:
    def __init__(self, display, window):
        self.display = display
        self.window = window
        self.DISPLAY_W, self.DISPLAY_H = self.display.get_size()
        self.running, self.playing = True, False
        self.font_name = "fonts/aesymatt.ttf"
        self.main_menu = MainMenu(self)
        self.login = LoginMenu(self)
        self.user_menu = UserMenu(self)
        self.signUp = SignUpMenu(self)
        self.createdUser = CreatedUser(self)
        self.ranking = RankingMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.clock = pygame.time.Clock()
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.ESCAPE_KEY = False, False, False, False

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(BLACK)
            self.draw_title_text("Thanks for playing", MENU_TEXT_SIZE, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0, 0))
            self.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                pygame.font.quit()
                pygame.quit()
                sys.exit(0)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        self.START_KEY = True
                    if event.key == pygame.K_ESCAPE:
                        self.ESCAPE_KEY = True
                    if event.key == pygame.K_DOWN:
                        self.DOWN_KEY = True
                    if event.key == pygame.K_UP:
                        self.UP_KEY = True
                if self.curr_menu in (self.login, self.signUp, self.ranking):
                    self.curr_menu.manager.process_events(event)
                    self.curr_menu.check_input(event, self.clock.tick(60) / 1000)
                elif self.curr_menu == self.createdUser:
                    self.curr_menu.check_input()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.ESCAPE_KEY = False, False, False, False

    def draw_text(self, text, size, x, y, color=WHITE):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.left = x
        text_rect.top = y
        self.display.blit(text_surface, text_rect)
        return text_rect

    def draw_title_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
        return text_rect

    def draw_success_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, GREEN)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
        return text_rect
