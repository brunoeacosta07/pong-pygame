import pygame_gui
from menus.menu import Menu, check_user
from utils.utils import *


def create_user(name, username, password):
    users = open_csv('resources/files/maestro-usuarios.csv')
    user_code = str(len(users) + 1).zfill(3)
    with open('resources/files/maestro-usuarios.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        # f.write('\n')
        writer.writerow([user_code, name, username, password])


class SignUpMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.name_x, self.name_y = INPUT_POS_X, login_box_height(self.mid_h, 1)
        self.username_x, self.username_y = INPUT_POS_X, login_box_height(self.mid_h, 2)
        self.password_x, self.password_y = INPUT_POS_X, login_box_height(self.mid_h, 3)
        self.confirm_password_x, self.confirm_password_y = INPUT_POS_X, login_box_height(self.mid_h, 4)

        self.manager = pygame_gui.UIManager((self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.name_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.name_x, self.name_y), (400, 50)),
            manager=self.manager,
            placeholder_text='Ingrese su nombre',
            object_id='#name_input'
        )
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
        self.confirm_password_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((self.confirm_password_x, self.confirm_password_y), (400, 50)),
            manager=self.manager,
            placeholder_text='Confirme su contraseña',
            object_id='#confirm_password_input',

        )
        self.confirm_password_input.set_text_hidden(True)
        self.submit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.confirm_password_x + 150, self.confirm_password_y + 100), (100, 50)),
            text='Crear usuario',
            manager=self.manager,
            object_id='#submit_button'
        )

        self.error_message = None

    async def display_menu(self):
        self.run_display = True

        while self.run_display:
            await self.game.check_events()
            self.game.display.fill(BLACK)
            self.game.draw_title_text('Crear usuario', TITLE_TEXT_SIZE + 30, self.mid_w, self.mid_h / 3)
            self.game.draw_text('Nombre:', MENU_TEXT_SIZE - 20, self.name_x - 135, self.name_y)
            self.game.draw_text('Usuario:', MENU_TEXT_SIZE - 20, self.username_x - 138, self.username_y)
            self.game.draw_text('Contraseña:', MENU_TEXT_SIZE - 20, self.password_x - 200, self.password_y)
            self.game.draw_text('Confirmar Contraseña:', MENU_TEXT_SIZE - 29, self.confirm_password_x - 290,
                                self.confirm_password_y+5)
            self.manager.draw_ui(self.game.display)

            if self.error_message:
                self.game.draw_text(self.error_message, 24, self.confirm_password_x, self.confirm_password_y + 55, RED)
            self.blit_screen()

    def tab_options(self):
        if self.name_input.is_focused:
            self.name_input.unfocus()
            self.username_input.focus()
        elif self.username_input.is_focused:
            self.username_input.unfocus()
            self.password_input.focus()
        elif self.password_input.is_focused:
            self.password_input.unfocus()
            self.confirm_password_input.focus()
        elif self.confirm_password_input.is_focused:
            self.confirm_password_input.unfocus()
            self.submit_button.focus()
        elif self.submit_button.is_focused:
            self.submit_button.unfocus()
            self.name_input.focus()

    def reset_inputs(self):
        self.name_input.set_text('')
        self.username_input.set_text('')
        self.password_input.set_text('')
        self.confirm_password_input.set_text('')

    def check_input(self, event, time_delta):
        if self.game.ESCAPE_KEY:
            self.reset_inputs()
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

        if self.game.START_KEY:
            self.validate_inputs()
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.submit_button:
                self.validate_inputs()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                self.tab_options()
        self.manager.update(time_delta)
        self.blit_screen()

    def validate_inputs(self):
        name = self.name_input.get_text()
        username = self.username_input.get_text()
        password = self.password_input.get_text()
        confirm_password = self.confirm_password_input.get_text()
        if not username and not password and not name and not confirm_password:
            self.error_message = "*Debe completar todos los campos*"
        elif not name:
            self.error_message = "*Debe completar el campo de nombre*"
        elif not username:
            self.error_message = "*Debe completar el campo de usuario*"
        elif not password:
            self.error_message = "*Debe completar el campo de contraseña*"
        elif not confirm_password:
            self.error_message = "*Debe completar el campo de confirmar contraseña*"
        else:
            self.error_message = None
            if check_user(username):
                self.error_message = "*El usuario ya existe*"
            else:
                if password == confirm_password:
                    create_user(name, username, password)
                    self.game.createdUser.user = username
                    self.game.curr_menu = self.game.createdUser
                    self.reset_inputs()
                    self.run_display = False
                else:
                    self.error_message = "*Las contraseñas no coinciden*"
