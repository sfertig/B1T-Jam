import pygame
from .utils import Assets

SC = "assets/images/screens/"

def LoadAssets():
    # -- images -- 
    #screens
    Assets.new_image("save_slot_bg", SC + "save_slot_screen.png", colorKey=None)
