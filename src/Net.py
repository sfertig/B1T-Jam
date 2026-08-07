import pygame

class _net:
    def __init__(self):
        #basics
        self.screen: pygame.Surface = None
        self.clock: pygame.time.Clock = None
        self.dt: float = 0.0

        self.events = None

Net = _net()
