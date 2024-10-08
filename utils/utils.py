import csv

import pygame
from pygame.locals import *

# Constants
WIDTH = 1118
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SPEED = 0.12
MENU_TEXT_SIZE = 55
TITLE_TEXT_SIZE = 75
OPTIONS_TEXT_POS = (WIDTH / 2) - 350
INPUT_POS_X = (WIDTH / 2) - 200
# MAIN MENU
LOGIN = 'LOGIN'
SIGNUP = 'SIGNUP'
REPORTS = 'REPORTS'
CREDITS = 'CREDITS'
# USER MENU
NEW_GAME = 'NEW_GAME'
LOAD_GAME = 'LOAD_GAME'
LOGOUT = 'LOGOUT'
# REPORTS MENU
USER_REGS = 'USER_REGS'
USER_QUERY = 'USER_QUERY'
RANKING = 'RANKING'
COLLISIONS = 'COLLISIONS'


def init_pygame():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Pong en Pygame")


def load_image(filename, transparent=False,):
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transparent:
        color = image.get_at((0, 0))
        image.set_colorkey(color, RLEACCEL)
    return image


def menu_text_height(mid_h, order):
    return (mid_h - 50) + (MENU_TEXT_SIZE / 2 + (order * 50))


def login_box_height(mid_h, order):
    return (mid_h - 200) + (MENU_TEXT_SIZE / 2 + (order * 70))


def open_csv(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def write_csv(file_path, data):
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
