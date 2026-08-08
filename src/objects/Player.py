import pygame

from ..utils import *
from ..Net import Net


class Player:
    def __init__(self, x, y):
        self.pos = Vector2D(x, y)
        self.vel = Vector2D(0, 0)
        self.speed = 50

        #set up animation manager
        anims = {
            "idle_right": Assets.get_animation("player_idle_right"),
            "idle_left": Assets.get_animation("player_idle_left"),
            "idle_front": Assets.get_animation("player_idle_front"),
            "idle_back": Assets.get_animation("player_idle_back"),
            "walk_right": Assets.get_animation("player_walk_right"),
            "walk_left": Assets.get_animation("player_walk_left"),
            "walk_front": Assets.get_animation("player_walk_front"),
            "walk_back": Assets.get_animation("player_walk_back"),
        }
        self.manager = AnimationManager(anims, "idle_front")
        self.dir = "front"


    def rect(self):
        return pygame.Rect((self.pos.x+4, self.pos.y+6), (8, 8))

    def input(self, events):
        self.vel = Vector2D(0.0, 0.0)
        if Keys.is_held(Keys.w): self.vel.y = -self.speed
        if Keys.is_held(Keys.a): self.vel.x = -self.speed
        if Keys.is_held(Keys.s): self.vel.y = self.speed
        if Keys.is_held(Keys.d): self.vel.x = self.speed

        self.update_anim()

    def update_anim(self):
        #update dir
        if self.vel.x < 0: self.dir = "left"
        elif self.vel.x > 0: self.dir = "right"
        elif self.vel.y < 0: self.dir = "back"
        elif self.vel.y > 0: self.dir = "front"

        #update animation
        if self.vel.x == 0 and self.vel.y == 0: self.manager.change_anim("idle_"+self.dir)
        else: self.manager.change_anim("walk_"+self.dir)


    def update(self, rects: list[pygame.Rect]):
        self.manager.update(Net.dt)
        self.input(Net.events)

        #x collisions
        self.pos.x += self.vel.x * Net.dt
        for rect in rects:
            if self.rect().colliderect(rect):
                if self.vel.x > 0: #right
                    self.pos.x -= self.vel.x * Net.dt
                    self.vel.x = 0
                elif self.vel.x < 0: #left
                    self.pos.x -= self.vel.x * Net.dt
                    self.vel.x = 0
        #y collisions
        self.pos.y += self.vel.y * Net.dt
        for rect in rects:
            if self.rect().colliderect(rect):
                if self.vel.y > 0: #down
                    self.pos.y -= self.vel.y * Net.dt
                    self.vel.y = 0
                elif self.vel.y < 0: #up
                    self.pos.y -= self.vel.y * Net.dt
                    self.vel.y = 0

        
    def render(self):
        image = self.manager.get_image()
        Net.screen.blit(image, (self.pos - Net.cam).to_int())



class ProgressBar:
    def __init__(self, x, y, width, height, min, max, value):
        self.pos = Vector2D(x, y)
        self.dim = Vector2D(width, height)
        self.min = min
        self.max = max
        self.value = value

    def rect(self):
        #get reletive how value is compared to min and max and width
        rel_width = (self.value - self.min) / (self.max - self.min) * self.dim.x
        rel_width = clamp(rel_width, 0, self.dim.x)
        if rel_width <= 1.0 and self.value > self.min: rel_width = 1
        return pygame.Rect(self.pos.to_int(), (rel_width, self.dim.y))

    def update(self, value):
        self.value = value

    def render(self, screen, cam: Vector2D):
        r = self.rect()
        r.topleft = (self.pos - cam).to_int()
        pygame.draw.rect(screen, (255, 255, 255), r)


