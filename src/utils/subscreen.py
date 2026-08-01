import pygame

from .math import Vector2D


class SubScreen:
    def __init__(self, x, y, w, h, bgColor: None, displaySurface: pygame.Surface = None):
        self.pos = Vector2D(x, y)
        self.dim = Vector2D(w, h)
        color = bgColor
        self.color = color
        self._screen = displaySurface
        if color == None: self.screen = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        else: self.screen = pygame.Surface((w, h)).convert()

    def clear(self):
        if self.color == None: self.screen.fill((0, 0, 0, 0))
        else: self.screen.fill(self.color)

    def local_mouse_pos(self):
        return Vector2D(*pygame.mouse.get_pos()) - self.pos


    def render(self, cam: Vector2D = Vector2D(0, 0)):
        self._screen.blit(self.screen, (self.pos - cam).to_int())