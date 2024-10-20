import concurrent.futures
import os
import csv
import asyncio
import pygame
import random
import requests
from datetime import datetime
import concurrent.futures
from pygame.locals import *
import google.generativeai as gemini

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

def generate_encouragement_message(player_score, cpu_score):
    player_winning_messages = [
        "¡Sigue así! Vas muy bien.",
        "¡Excelente trabajo! Mantén el ritmo.",
        "¡Estás en racha! No te detengas.",
        "¡Impresionante! Sigue acumulando puntos."
    ]

    cpu_winning_messages = [
        "¡Sigue intentando, no desistas!",
        "¡No te rindas! Puedes darle la vuelta.",
        "¡Ánimo! Todavía hay tiempo para ganar.",
        "¡No te preocupes! La próxima será mejor."
    ]

    if player_score > cpu_score:
        return random.choice(player_winning_messages)
    else:
        return random.choice(cpu_winning_messages)


async def gemini_generative_text(player, cpu):
    gemini.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = gemini.GenerativeModel('gemini-1.5-flash')

    loop = asyncio.get_event_loop()

    with (concurrent.futures.ThreadPoolExecutor() as pool):

        response = await loop.run_in_executor(
            pool,
            model.generate_content,
            "Teniendo en cuenta la siguiente puntuacion y como si se siguiera jugando," +
                                      " genera un muy breve texto de aliento o felicitaciones " +
                                      "(sin incluir el puntaje en la respuesta), segun corresponda. " +
                                      f"Jugador: {player}, cpu: {cpu}"
        )
    if response.candidates and response.candidates[0].finish_reason:
        return response.text
    else:
        print("Mensaje default")
        return generate_encouragement_message(player, cpu)


async def update_game_info(game, playing):
    url = 'https://game-status-back.onrender.com/game-info'
    data = {
        'matchNumber': game.match_number,
        'player1': {
            'name': game.user_menu.user['usuario'],
            'points': game.scores[0]
        },
        'player2': {
            'name': 'CPU',
            'points': game.scores[1]
        },
        'playing': playing,
        'matchDate': datetime.now().strftime('%Y-%m-%d')
    }
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        response = await loop.run_in_executor(
            pool,
            lambda: requests.post(url, json=data)
        )
    if response.status_code == 201:
        print("Informacion de la partida actualizada exitosamente")
    else:
        print("Error al actualizar la informacion de la partida")
