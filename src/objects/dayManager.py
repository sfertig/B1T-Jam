import pygame

from .Player import ProgressBar

from ..utils import Vector2D, Assets, Keys, Timer, SubScreen

DAY_LENGTH = 120 #seconds

class DayManager:
    def __init__(self, screen):
        self.day = 1
        self.bar = ProgressBar(14, 7, 53, 2, 0, DAY_LENGTH, 0)
        self.subscreen = SubScreen(128, 0, 80, 16, "black", screen)
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

class House:
    def __init__(self, screen, cam):
        self.image = Assets.get_image("house")
        self.subscreen = SubScreen(-368, 0, 368, 360, "black", screen)
        self.screen = self.subscreen.screen
        self.workbench_rect = pygame.Rect(304, 35, 43, 11)
        self.show_workbench_btn = False
        self.cam: Vector2D = cam

    def update(self, dt, events, player):
        r = self.subscreen.get_global_rect(self.workbench_rect.copy())
        if r.colliderect(player.rect()):
            self.show_workbench_btn = True
            self.cam.y = -100
        else:
            self.show_workbench_btn = False
            self.cam.y = 0
        

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.screen.blit(self.image, (0, 0))
        if self.show_workbench_btn:
            pass #display show
        #update
        self.subscreen.render(cam)

