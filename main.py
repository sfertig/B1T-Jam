import asyncio
import pygame
import sys
import os

from src.codes import *
from src.screens import Title_screen
from src.utils import Assets

IM = "assets/images/"

def load_assets():
    #player idle anims
    Assets.new_anim_nIMG("player_idle_right", size=16, fps=3, path=IM+"player.png", rect=(0, 0, 32, 16))
    Assets.animations["player_idle_left"] = Assets.get_animation("player_idle_right").copy()
    Assets.animations["player_idle_left"].flip_h()
    Assets.new_anim_nIMG("player_idle_front", size=16, fps=3, path=IM+"player.png", rect=(0, 16, 32, 16))
    Assets.new_anim_nIMG("player_idle_back", size=16, fps=3, path=IM+"player.png", rect=(0, 32, 32, 16))
    #player walk anims
    Assets.new_anim_nIMG("player_walk_right", size=16, fps=3, path=IM+"player.png", rect=(32, 0, 32, 16))
    Assets.animations["player_walk_left"] = Assets.get_animation("player_walk_right").copy()
    Assets.animations["player_walk_left"].flip_h()
    Assets.new_anim_nIMG("player_walk_front", size=16, fps=3, path=IM+"player.png", rect=(32, 16, 32, 16))
    Assets.new_anim_nIMG("player_walk_back", size=16, fps=3, path=IM+"player.png", rect=(32, 32, 32, 16))


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

    load_assets()

    clock = pygame.time.Clock()
    
    state = TITLE_SCREEN

    while True:
        if state == TITLE_SCREEN: state = await Title_screen(screen, clock).run()
        elif state == SHUT_DOWN and not IS_WEB: break #web version should not fully shut down
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())

