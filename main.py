import asyncio
import pygame
import sys
import os

from src.codes import *
from src.screens import *
from src.utils import Assets



pygame.init()

# Check if running in WebAssembly (Browser)
IS_WEB = sys.platform == "emscripten"

async def main():

    width, height = 640, 360
    if IS_WEB:
        # Web build: rely on SCALED (pygbag handles window fit)
        screen = pygame.display.set_mode((width, height))
    else:
        # Desktop build: full experience with SCALED + FULLSCREEN
        screen = pygame.display.set_mode(
            (width, height), pygame.SCALED | pygame.FULLSCREEN
        )
    pygame.display.set_caption("test title")

    #load_assets(IS_WEB)

    clock = pygame.time.Clock()
    
    state = TITLE_SCREEN

    while True:
        if state == TITLE_SCREEN: state = await Title_screen(screen, clock).run()
        elif state == SHUT_DOWN and not IS_WEB: break #web version should not fully shut down
        elif state == GAME_SCREEN: state = await Game_screen(screen, clock).run()
        elif state == TUTORIAL: state = await Tutorial(screen, clock).run()
    pygame.quit()
    if not IS_WEB: os.system('cls')

if __name__ == "__main__":
    asyncio.run(main())

