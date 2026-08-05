import pygame

from ..utils import *
from .Player import ProgressBar, Player
from .Tile import TILLING_COST, MIN_TILLING_COST
from .shop import Shop

class House:
    def __init__(self, screen, cam):
        self.image = Assets.get_image("house")
        self.subscreen = SubScreen(-80, 0, 80, 352, "black", screen)
        self.screen = self.subscreen.screen
        self.workbench_rect = pygame.Rect(20, 99, 41, 12)
        self.show_workbench_btn = False
        self.shop = Shop(screen, cam)
        self.cam: Vector2D = cam

        self.bed_rect = pygame.Rect(16, 176, 48, 16)
        self.bed_show_e = False

    def update(self, dt, events, player):
        r = self.subscreen.get_global_rect(self.workbench_rect.copy())
        if r.colliderect(player.rect()):
            self.show_workbench_btn = True
            #self.cam.y = -110
        else:
            self.show_workbench_btn = False
            self.cam.y = 0

        if self.show_workbench_btn:
            self.shop.update(dt, events, player)

        #bed
        r = self.subscreen.get_global_rect(self.bed_rect.copy())
        if r.colliderect(player.rect()):
            self.bed_show_e = True
        else:
            self.bed_show_e = False
        

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.screen.blit(self.image, (0, 0))
        if self.show_workbench_btn:
            self.shop.render(screen, cam)

        if self.bed_show_e:
            self.screen.blit(Assets.get_image("btn_e"), Vector2D(32, 160).to_int())

        #update
        self.subscreen.render(cam)