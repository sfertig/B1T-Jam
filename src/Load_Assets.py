import pygame
from .utils import Assets

SC = "assets/images/screens/"
AM = "assets/images/animations/"
MU = "assets/images/menues/"
OP = "assets/images/objects/"

def LoadAssets():
    # -- images -- 

    # - screens -
    #save slot assets
    Assets.new_image("save_slot_outline", SC + "save_slot_screen.png", rect=(0, 0, 98, 138))
    Assets.new_image("save_slot_empty", SC + "save_slot_screen.png", rect=(112, 0, 64, 16))
    Assets.new_image("save_slot_create", SC + "save_slot_screen.png", rect=(112, 16, 64, 16))
    Assets.new_image("save_slot_clear", SC + "save_slot_screen.png", rect=(112, 32, 64, 16))
    Assets.new_image("save_slot_play", SC + "save_slot_screen.png", rect=(112, 48, 64, 16))

    # - objects -
    #plants
    Assets.new_image("pt_none", OP + "plant_tiles.png", rect=(0, 0, 16, 16))
    Assets.new_image("pt_wheat_resting", OP + "plant_tiles.png", rect=(16, 0, 16, 16))
    Assets.new_image("pt_wheat_tilled", OP + "plant_tiles.png", rect=(32, 0, 16, 16))
    Assets.new_image("pt_wheat_growing", OP + "plant_tiles.png", rect=(48, 0, 16, 16))
    Assets.new_image("pt_wheat_grown", OP + "plant_tiles.png", rect=(64, 0, 16, 16))
    

    # -- animations --

    # - player -
    #player idle anims
    Assets.new_anim_nIMG("player_idle_right", size=16, fps=3, path=AM+"player.png", rect=(0, 0, 32, 16))
    Assets.animations["player_idle_left"] = Assets.get_animation("player_idle_right").copy()
    Assets.animations["player_idle_left"].flip_h()
    Assets.new_anim_nIMG("player_idle_front", size=16, fps=3, path=AM+"player.png", rect=(0, 16, 32, 16))
    Assets.new_anim_nIMG("player_idle_back", size=16, fps=3, path=AM+"player.png", rect=(0, 32, 32, 16))
    #player walk anims
    Assets.new_anim_nIMG("player_walk_right", size=16, fps=3, path=AM+"player.png", rect=(32, 0, 32, 16))
    Assets.animations["player_walk_left"] = Assets.get_animation("player_walk_right").copy()
    Assets.animations["player_walk_left"].flip_h()
    Assets.new_anim_nIMG("player_walk_front", size=16, fps=3, path=AM+"player.png", rect=(32, 16, 32, 16))
    Assets.new_anim_nIMG("player_walk_back", size=16, fps=3, path=AM+"player.png", rect=(32, 32, 32, 16))

    # -- menues --
    Assets.new_image("pause_ui", MU+"pause_menu.png")

