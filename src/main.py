import pygame
from game import Game
from menu import Menu
from settings import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Guitar Hero Clone")

    menu = Menu(screen)
    choice = menu.run()

    if choice == "start_game":
        game = Game(screen)
        game.run()
    pygame.quit()


if __name__ == "__main__":
    main()
