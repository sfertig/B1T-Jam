import pygame
from ..utils import Assets
from ..Net import Net
from ..objects import *

def INITSAVEDATA(data, p: Player):
    Net.cam.x, Net.cam.y = data["cam_offset"]

    p.pos.x, p.pos.y = data["player_pos"]

