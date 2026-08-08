import pygame

from .utils.versions import load_settings

def INITSETTINGS(net):
    data = load_settings()
    net.FPS = data["fps"]
    pygame.display.set_caption(data["title"])


class _net:
    def __init__(self):
        #basics
        self.screen: pygame.Surface = None
        self.clock: pygame.time.Clock = None
        self.FPS = 60
        self.dt: float = 0.0

        self.events = None

    def init(self):
        INITSETTINGS(self)

Net = _net()
