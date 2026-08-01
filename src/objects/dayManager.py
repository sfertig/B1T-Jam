import pygame

from .Player import ProgressBar

from ..utils import Vector2D, Assets, Keys, Timer, SubScreen

DAY_LENGTH = 120 #seconds

class DayManager:
    def __init__(self, screen):
        self.day = 1
        self.bar = ProgressBar(14, 7, 53, 2, 0, DAY_LENGTH, 0)
        self.subscreen = SubScreen(528, 0, 80, 16, "black", screen)
        self.screen = self.subscreen.screen
        self.timer = Timer(DAY_LENGTH)

    def update(self, dt, events):
        self.timer.update(dt)

        self.bar.update(int(self.timer.get_time()))

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.screen.blit(Assets.get_image("day_ui"), (0, 0))
        self.bar.render(self.screen, Vector2D(0, 0))
        #update
        self.subscreen.render(cam)

