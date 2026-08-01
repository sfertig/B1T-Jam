import pygame

from ..utils import Vector2D, Assets, Keys

class Tile:
    def __init__(self, x, y, type):
        self.pos = Vector2D(x, y)
        self.type = type

    def update(self, dt, events):
        pass

    def render(self, screen, cam):
        pass

