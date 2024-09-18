import pygame_gui
from menus.menu import Menu, check_user
from utils.utils import *


def check_credentials(username, password):
    users = open_csv('resources/files/maestro-usuarios.csv')
    for user in users:
        if user['usuario'].lower() == username.lower() and user['clave'] == password:
            return True
    return False


class LoginMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.username_x, self.username_y = self.mid_w - 200, login_box_height(self.mid_h, 1)
        self.password_x, self.password_y = self.mid_w - 200, login_box_height(self.mid_h, 2.5)

        self.manager = pygame_gui.UIManager((self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.username_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.username_x, self.username_y), (400, 50)),
            manager=self.manager,
            placeholder_text='Ingrese su usuario',
            object_id='#username_input'
        )
        self.password_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.password_x, self.password_y), (400, 50)),
            manager=self.manager,
            placeholder_text='Ingrese su contraseña',
            object_id='#password_input',

        )
        self.password_input.set_text_hidden(True)
        self.submit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.password_x + 150, self.password_y + 100), (100, 50)),
            text='Ingresar',
            manager=self.manager,
            object_id='#submit_button'
        )
        self.error_message = None

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()
            self.game.display.fill(BLACK)
            self.game.draw_title_text('Login', TITLE_TEXT_SIZE+30, self.mid_w, self.mid_h / 3)
            self.game.draw_text('Usuario:', MENU_TEXT_SIZE - 20, self.username_x - 135, self.username_y)
            self.game.draw_text('Contraseña:', MENU_TEXT_SIZE - 20, self.password_x - 200, self.password_y)
            self.manager.draw_ui(self.game.display)

            if self.error_message:
                self.game.draw_text(self.error_message, 24, self.password_x, self.password_y + 55, RED)
            self.blit_screen()

    def check_input(self, event, time_delta):
        if self.game.ESCAPE_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.validate_inputs()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.submit_button:
                self.validate_inputs()
        self.manager.update(time_delta)
        self.blit_screen()

    def validate_inputs(self):
        username = self.username_input.get_text()
        password = self.password_input.get_text()
        if not username and not password:
            self.error_message = "*Debe completar todos los campos*"
        elif not username:
            self.error_message = "*Debe completar el campo de usuario*"
        elif not password:
            self.error_message = "*Debe completar el campo de contraseña*"
        else:
            self.error_message = None
            if check_user(username):
                if check_credentials(username, password):
                    print("Credenciales correctas")
                else:
                    self.error_message = "*contraseña incorrecta*"
            else:
                self.error_message = "*Usuario inexistente*"

