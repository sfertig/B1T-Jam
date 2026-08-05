import pygame

from ..utils import *

SCARE = 5

class ScareCrow:
    def __init__(self, x, y, tx, ty, cam: Vector2D, screen):
        self.pos = Vector2D(x, y)
        self.tPos = Vector2D(tx, ty)
        self.image = Assets.get_image("hilight")
        self.rect = pygame.Rect((x, y), (16, 16))
        self.cam = cam

        self.subscreen = SubScreen(tx, ty, 64, 32, "black", screen)
        self.ui = Assets.get_image("scarecrow_ui")
        self.screen = self.subscreen.screen

        self.show_ui = False
        self.built = False

    def update(self, dt, events, player):
        if self.built: return
        if self.cam.to_int() == (0, 0):
            if self.rect.colliderect(player.rect()):
                self.show_ui = True
                if Keys.is_pressed(Keys.e, events) and player.take_money(10): 
                    self.image = Assets.get_image("scarecrow")
                    self.built = True
                    self.show_ui = False
            else:
                self.show_ui = False

    def render(self, screen, cam: Vector2D):
        screen.blit(self.image, (self.pos.x - self.cam.x, self.pos.y - self.cam.y))
        if self.show_ui:
            self.subscreen.clear()
            self.screen.blit(self.ui, (0, 0))
            self.subscreen.render(cam)

class ScareCrow_Manager:
    def __init__(self, cam, screen):
        
        
        self.crows = [
            ScareCrow(608, 16, 544, 16, cam, screen),
            ScareCrow(608, 320, 560, 288, cam, screen),
            ScareCrow(128, 320, 104, 288, cam, screen),
            ScareCrow(128, 16, 104, 32, cam, screen),
        ]
        self.cam = cam

    def update(self, dt, events, player):
        for crow in self.crows:
            crow.update(dt, events, player)

    def get_built(self):
        num = 0
        for crow in self.crows:
            if crow.built:
                num += 1
        return num*SCARE

    def render(self, screen, cam: Vector2D):
        for crow in self.crows:
            crow.render(screen, cam)
