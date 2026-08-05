import pygame

from .Player import ProgressBar, Player
from .Tile import TILLING_COST, MIN_TILLING_COST

from ..utils import Vector2D, Assets, Keys, Timer, SubScreen

DAY_LENGTH = 200 #seconds
SLEEP_WIDTH = 45

class DayManager:
    def __init__(self, screen):
        self.day = 1
        self.bar = ProgressBar(14, 7, 53, 2, 0, DAY_LENGTH, 0)
        self.subscreen = SubScreen(128, 0, 80, 16, "black", screen)
        self.screen = self.subscreen.screen
        self.timer = Timer(DAY_LENGTH)


    def update(self, dt, events, player):
        self.timer.update(dt)

        self.bar.update(int(self.timer.get_time()))

    def sleep(self):
        global DAY_LENGTH
        self.day += 1
        self.bar.value = 0
        DAY_LENGTH -= 5
        self.bar.max = DAY_LENGTH
        self.timer = Timer(DAY_LENGTH)

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.screen.blit(Assets.get_image("day_ui"), (0, 0))
        self.bar.render(self.screen, Vector2D(0, 0))
        #update
        self.subscreen.render(cam)
