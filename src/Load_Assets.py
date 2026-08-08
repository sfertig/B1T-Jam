import pygame
from .utils import Assets

SC = "assets/images/screens/"

def LoadAssets():
    # -- images -- 
    # - screens -
    #save slot assets
    Assets.new_image("save_slot_outline", SC + "save_slot_screen.png", rect=(0, 0, 98, 138))
    Assets.new_image("save_slot_empty", SC + "save_slot_screen.png", rect=(112, 0, 64, 16))
    Assets.new_image("save_slot_create", SC + "save_slot_screen.png", rect=(112, 16, 64, 16))
    Assets.new_image("save_slot_clear", SC + "save_slot_screen.png", rect=(112, 32, 64, 16))
    Assets.new_image("save_slot_play", SC + "save_slot_screen.png", rect=(112, 48, 64, 16))
