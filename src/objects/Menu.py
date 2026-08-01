import pygame

from ..codes import *
from ..utils import *

class PauseMenu:
    def __init__(self, screen):
        self.image = Assets.get_image("pause_ui")
        self.subscreen = SubScreen(192, 48, 240, 240, "black", screen)
        self.screen = self.subscreen.screen
        self.active = False

        self.resume = pygame.Rect(39, 104, 161, 32)
        self.quit = pygame.Rect(39, 168, 161, 32)

    def update(self, dt, events):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = self.subscreen.local_mouse_pos().to_int()
            if self.resume.collidepoint(mouse_pos):
                self.active = False
            elif self.quit.collidepoint(mouse_pos):
                return SHUT_DOWN
        return None

    def render(self):
        self.subscreen.clear()
        #render
        self.screen.blit(self.image, (0, 0))
        #update
        self.subscreen.render()
