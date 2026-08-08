import pygame
import sys
from .utils.versions import *
from .utils import Vector2D

def INITSETTINGS(net):
    data = load_settings()
    net.FPS = data["fps"]
    pygame.display.set_caption(data["title"])
    net.settings = data

    net.slot_1 = load_save_file(1)
    net.slot_2 = load_save_file(2)
    net.slot_3 = load_save_file(3)



class _net:
    def __init__(self):
        #basics
        self.screen: pygame.Surface = None
        self.clock: pygame.time.Clock = None
        self.FPS = 60
        self.dt: float = 0.0
        self.click = False

        self.selected_slot = None

        self.events = None
        self.build = False

        self.cam: Vector2D = Vector2D(0, 0)

        #save data
        self.settings = {}
        self.slot_1 = {}
        self.slot_2 = {}
        self.slot_3 = {}

    def shut_down(self):
        #save
        save_settings(self.settings)
        save_all_saves(self.slot_1, self.slot_2, self.slot_3)
        #exit
        pygame.quit()
        sys.exit()

    def init(self):
        INITSETTINGS(self)

Net = _net()
