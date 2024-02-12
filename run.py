import pygame
from menus.Menu import Menu


def run() -> None:

    pygame.init()
    pygame.font.init()

    menu = Menu()
    menu.run()


if __name__ == "__main__":
    run()