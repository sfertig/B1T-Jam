import pygame

from ..utils import Keys, Vector2D, Assets, AnimationManager


class Player:
    def __init__(self, x, y):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D(0, 0)
        self.speed = 200

    def rect(self):
        return pygame.Rect(self.pos.to_int(), (16, 16))

    def input(self, events):
        self.vel = Vector2D(0.0, 0.0)
        if Keys.is_held(Keys.w): self.vel.y = -self.speed
        if Keys.is_held(Keys.a): self.vel.x = -self.speed
        if Keys.is_held(Keys.s): self.vel.y = self.speed
        if Keys.is_held(Keys.d): self.vel.x = self.speed

    def update(self, dt, events):
        self.input(events)

        self.pos += (self.vel*dt)
        #TODO: add collision


    def render(self, screen, cam: Vector2D):
        r = self.rect()
        r.topleft = (self.pos-cam).to_int()
        pygame.draw.rect(screen, "green", r, 1)
