import asyncio
import pygame
import sys
import os

from src.codes import *
from src.screens import *
from src.utils import Assets

IM = "assets/images/"
FT = "assets/fonts/"

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
    #images
    Assets.new_image("game_bg", IM+"bg_image.png")
    Assets.new_image("tile_dead", IM+"tiles.png", rect=(32, 0, 16, 16))
    Assets.new_image("tile_resting", IM+"tiles.png", rect=(16, 0, 16, 16))
    Assets.new_image("tile_tilled", IM+"tiles.png", rect=(0, 0, 16, 16))
    Assets.new_image("tile_growing", IM+"tiles.png", rect=(48, 0, 16, 16))
    Assets.new_image("tile_grown", IM+"tiles.png", rect=(0, 16, 16, 16))
    Assets.new_image("tile_none", IM+"tiles.png", rect=(16, 16, 16, 16))
    #images - buttons
    Assets.new_image("btn_e", IM+"buttons.png", rect=(0, 0, 16, 16), colorKey=None)
    Assets.new_image("inventory_ui", IM+"inventory_ui.png", colorKey=None)
    Assets.new_image("day_ui", IM+"day_ui.png", colorKey=None)
    Assets.new_image("pause_ui", IM+"pause_menu.png", colorKey=None)
    Assets.new_image("house", IM+"house.png", colorKey=None)
    Assets.new_image("shop", IM+"shop.png", colorKey=None)
    Assets.new_image("death_ui", IM+"death_screen.png", colorKey=None)
    #font
    #Assets.new_font("font", FT+"pixelFont.ttf", 20)


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
    
    state = GAME_SCREEN #TITLE_SCREEN

    while True:
        if state == TITLE_SCREEN: state = await Title_screen(screen, clock).run()
        elif state == SHUT_DOWN and not IS_WEB: break #web version should not fully shut down
        elif state == GAME_SCREEN: state = await Game_screen(screen, clock).run()
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())

