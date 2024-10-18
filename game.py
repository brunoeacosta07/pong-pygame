from datetime import datetime
from random import Random

from menus.created_user import CreatedUser
from menus.credits_menu import CreditsMenu
from menus.login_menu import LoginMenu
from menus.main_menu import MainMenu
from menus.reports_menu import ReportsMenu
from menus.signup_menu import SignUpMenu
from menus.user_menu import UserMenu
from sprites.ball import Ball
from sprites.paddle import Paddle
from sprites.text import Text
from utils.utils import *
import sys


def write_collision_detail(collision):
    with open('resources/files/detalle-colisiones.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(collision)


def append_match_statics(user_code, match_number, score_player, score_cpu):
    with open('resources/files/detalle-partida-jugador.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        date = datetime.now().strftime('%d-%m-%Y')
        writer.writerow([user_code, match_number, score_player, score_cpu, date])


def update_match_statics(user_code, match_number, score_player, score_cpu):
    matches = open_csv('resources/files/detalle-partida-jugador.csv')
    for match in matches:
        if match['codUsuario'] == str(user_code) and match['numPartida'] == str(match_number):
            match['puntajeA'] = score_player
            match['puntajeB'] = score_cpu
            date = datetime.now().strftime('%d-%m-%Y')
            match['fechaPartida'] = date
    write_csv('resources/files/detalle-partida-jugador.csv', matches)


def append_match(match_number):
    with open('resources/files/acumulador-partidas.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        match_id = str(match_number).zfill(3)
        writer.writerow([match_id, match_number])


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
        self.reports = ReportsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.clock = pygame.time.Clock()
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.ESCAPE_KEY = False, False, False, False
        self.background_image = pygame.transform.scale(load_image('resources/img/background_tenis.png'),
                                                       (WIDTH, HEIGHT))
        self.balls = {
            0: {0: Ball(1)},
            1: {0: Ball(2, initial_y=Random().randint(0, HEIGHT))},
            2: {0: Ball(3, initial_y=Random().randint(0, HEIGHT))}
        }

        self.balls[1][0].speed = [-self.balls[1][0].speed[0], -self.balls[1][0].speed[1]]
        self.balls[2][0].speed = [SPEED, SPEED]
        self.player_paddle = Paddle(30)
        self.player_paddle.speed += 0.8
        self.cpu_paddle = Paddle(WIDTH - 30)
        self.cpu_paddle.speed += 0.2
        self.cpu_paddle.target_ball = self.balls[0][0]
        self.text = Text(font_name=self.font_name)
        self.scores = [0, 0]
        self.collision_rect = [0, 0]
        self.match_number = 0
        self.match_message = None
        self.message_x = WIDTH
        self.last_score = 0

    async def game_loop(self):
        while self.playing:
            self.check_events()
            time = self.clock.tick(60)
            keys = pygame.key.get_pressed()
            for i in range(len(self.balls)):
                self.balls[i][0].update(time+1, self.player_paddle, self.cpu_paddle, self.scores)
            self.collide_balls()
            self.player_paddle.move(time, keys)
            self.cpu_paddle.ai(time)
            self.cpu_paddle.update_target_ball([self.balls[i][0] for i in range(len(self.balls))])
            self.build_collision_detail()
            self.window.blit(self.background_image, (0, 0))
            self.text.render(self.window, f"{self.user_menu.user['usuario'].upper()}: "
                                          f"{self.scores[0]}", WHITE, (20, 10))
            self.text.render(self.window, f"CPU: {self.scores[1]}", WHITE, (WIDTH - 150, 10))
            self.display_match_message(time)
            for i in range(len(self.balls)):
                self.window.blit(self.balls[i][0].image, self.balls[i][0].rect)
            self.window.blit(self.player_paddle.image, self.player_paddle.rect)
            self.window.blit(self.cpu_paddle.image, self.cpu_paddle.rect)
            pygame.display.flip()
            self.reset_keys()

            if self.scores[0] % 10 == 0 and self.scores[0] != self.last_score:
                print('entro a gemini')
                self.last_score = self.scores[0]
                asyncio.create_task(self.run_gemini_generative_text())
            await asyncio.sleep(0)

    async def run_gemini_generative_text(self):
        player_score = self.scores[0]
        cpu_score = self.scores[1]
        print('iniciando gemini')
        self.match_message = await gemini_generative_text(player_score, cpu_score)
        print(self.match_message)

    def display_match_message(self, time):
        if self.match_message:
            text_rect = self.text.blit_text(self.window,self.match_message, self.message_x, HEIGHT - 70)
            self.message_x -= 0.1 * time
            if text_rect.right < 0:
                self.match_message = None
                self.message_x = WIDTH

    def update_match_data(self):
        matches = open_csv('resources/files/acumulador-partidas.csv')
        exists_match = [match for match in matches if match['acumPartida'] == str(self.match_number)] != []

        if not exists_match:
            append_match(self.match_number)
            append_match_statics(self.user_menu.user['codUsuario'], self.match_number, self.scores[0], self.scores[1])
        else:
            update_match_statics(self.user_menu.user['codUsuario'], self.match_number, self.scores[0], self.scores[1])

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.update_match_data()
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
                if self.curr_menu in (self.login, self.signUp, self.reports.ranking, self.user_menu.rankingMenu,
                                      self.reports.user_query, self.reports.collisions, self.user_menu.loadMenu,
                                      self.reports.user_regs):
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

    def collide_balls(self):
        balls = [self.balls[i][0] for i in range(len(self.balls))]
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):
                if balls[i].rect.colliderect(balls[j].rect):
                    balls[i].speed[0] = -balls[i].speed[0]
                    balls[j].speed[0] = -balls[j].speed[0]
                    balls[i].speed[1] = -balls[i].speed[1]
                    balls[j].speed[1] = -balls[j].speed[1]

                    overlap_x = ((balls[i].rect.width + balls[j].rect.width) / 2 -
                                 abs(balls[i].rect.centerx - balls[j].rect.centerx))
                    overlap_y = ((balls[i].rect.height + balls[j].rect.height) / 2 -
                                 abs(balls[i].rect.centery - balls[j].rect.centery))

                    if overlap_x < overlap_y:
                        if balls[i].rect.centerx < balls[j].rect.centerx:
                            balls[i].rect.centerx -= overlap_x / 2
                            balls[j].rect.centerx += overlap_x / 2
                        else:
                            balls[i].rect.centerx += overlap_x / 2
                            balls[j].rect.centerx -= overlap_x / 2
                    else:
                        if balls[i].rect.centery < balls[j].rect.centery:
                            balls[i].rect.centery -= overlap_y / 2
                            balls[j].rect.centery += overlap_y / 2
                        else:
                            balls[i].rect.centery += overlap_y / 2
                            balls[j].rect.centery -= overlap_y / 2

    def build_collision_detail(self):
        observation = self.get_collision()
        if observation:
            cod_user = self.user_menu.user['codUsuario']
            date = datetime.now().strftime('%Y-%m-%d')
            collision = f"Colision en x={self.collision_rect[0]}, y={self.collision_rect[1]}"
            write_collision_detail([cod_user, self.match_number, date, collision, observation])

    def get_collision(self):
        balls = [self.balls[i][0] for i in range(len(self.balls))]
        for i in range(len(balls)):
            if self.player_paddle.rect.colliderect(balls[i].rect) and balls[i].speed[0] > 0:
                self.collision_rect = [balls[i].rect.centerx, balls[i].rect.centery]
                return f"(1|{balls[i].number})"
            elif self.cpu_paddle.rect.colliderect(balls[i].rect) and balls[i].speed[0] < 0:
                return f"(2|{balls[i].number})"
        return None
