import pygame
import sys
import pygame_gui

pygame.init()

WIDTH, HEIGHT = 1118, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Input")

CLOCK = pygame.time.Clock()
MANAGER = pygame_gui.UIManager((WIDTH, HEIGHT))
text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 200), (140, 32)), manager=MANAGER, object_id="#main_text_entry")


def show_text(text):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        SCREEN.fill("white")

        new_text = pygame.font.SysFont("bahnschrift", 100).render(f"Hello, {text}", True, "black")
        new_text_rect = new_text.get_rect(center=(WIDTH/2, HEIGHT/2))
        SCREEN.blit(new_text, new_text_rect)

        CLOCK.tick(60)
        pygame.display.update()


def get_user_name():
    while True:
        UI_REFRESH_RATE = CLOCK.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
                show_text(event.text)

            MANAGER.process_events(event)

        MANAGER.update(UI_REFRESH_RATE)
        SCREEN.fill("white")
        MANAGER.draw_ui(SCREEN)
        pygame.display.update()


get_user_name()
