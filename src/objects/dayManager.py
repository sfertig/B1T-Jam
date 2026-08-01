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
        self.shop = Shop(screen)
        self.cam: Vector2D = cam

    def update(self, dt, events, player):
        r = self.subscreen.get_global_rect(self.workbench_rect.copy())
        if r.colliderect(player.rect()):
            self.show_workbench_btn = True
            self.cam.y = -115
        else:
            self.show_workbench_btn = False
            self.cam.y = 0

        if self.show_workbench_btn:
            self.shop.update(dt, events, player)
        

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.screen.blit(self.image, (0, 0))
        if self.show_workbench_btn:
            self.shop.render(screen, cam)
        #update
        self.subscreen.render(cam)

class Shop:
    def __init__(self, screen):
        self.image = Assets.get_image("shop")
        self.subscreen = SubScreen(-368, -105, 368, 100, "black", screen)
        self.screen = self.subscreen.screen
        self.seeds_rect = pygame.Rect(16, 16, 32, 16)
        self.hoe_rect = pygame.Rect(16, 38, 32, 16)

    def update(self, dt, events, player):
        pass

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.screen.blit(self.image, (0, 0))

        #debug
        pygame.draw.rect(self.screen, (255, 0, 0), self.seeds_rect, 1)
        pygame.draw.rect(self.screen, (255, 0, 0), self.hoe_rect, 1)
        #update
        self.subscreen.render(cam)

