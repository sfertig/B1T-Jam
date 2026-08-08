import pygame
from ..utils import Assets
from ..Net import Net
from ..objects import *

def INITSAVEDATA(data: dict, p: Player):
    Net.cam.x, Net.cam.y = data.get("cam_offset", (0, 0))

    p.pos.x, p.pos.y = data.get("player_pos", (0, 0))

def SAVEDATA(data: dict, p: Player):
    data["cam_offset"] = (Net.cam.x, Net.cam.y)
    data["player_pos"] = (p.pos.x, p.pos.y)
    

