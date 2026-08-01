import pygame
import random

from ..utils import Vector2D, Assets, Keys, Timer

TILLING_COST = 10
DEAD_COST = 25

MIN_GROW_TIME = 20
MAX_GROW_TIME = 45

MIN_REST_TIME = 20
MAX_REST_TIME = 45

MIN_TILLED_TIME = 20
MAX_TILLED_TIME = 45

MIN_DEATH_TIME = 20 #TODO: add return to death state in night time
MAX_DEATH_TIME = 45

class Tile:
    def __init__(self, x, y, type):
        self.pos = Vector2D(x, y)
        self.type = type
        self.image = None
        self.rect = pygame.Rect((x, y), (16, 16))
        if self.type not in ["dead", "resting", "tilled", "growing", "grown"]:
            raise ValueError(f"Invalid tile type: {self.type}")

        self.set_image()
        self.show_btn = False

        self.timer = Timer(random.randint(MIN_GROW_TIME, MAX_GROW_TIME))
        self.cooldown = False

    def set_image(self):
        self.image = Assets.get_image(f"tile_{self.type}")
    def set_show_btn(self, player):
        if self.type in ["tilled", "resting", "grown", "dead"] and player.rect().colliderect(self.rect) and not self.cooldown:self.show_btn = True
        else: self.show_btn = False

    def set_timer(self, min=MIN_GROW_TIME, max=MAX_GROW_TIME, cool=False):
        self.timer = Timer(random.randint(min, max))
        self.cooldown = cool
        print(self.cooldown, cool)

    def update(self, dt, events, player):

        self.set_show_btn(player)

        if self.cooldown:
            self.timer.update(dt)
            if self.timer.is_done(): self.cooldown = False

        if self.type == "growing":
            self.timer.update(dt)
            if self.timer.is_done():
                self.type = "grown"
                self.set_image()
                self.set_timer()

        if self.show_btn and Keys.is_pressed(Keys.e, events):
            if self.type == "tilled" and player.seeds > 0:
                self.type = "growing"
                self.set_image()
                player.seeds -= 1
            elif self.type == "grown":
                self.set_timer(MIN_REST_TIME, MAX_REST_TIME, cool=True)
                self.type = "resting"
                player.plants += 1
                self.set_image()
            elif self.type == "resting" and player.hoe_durability > 0:
                self.set_timer(MIN_TILLED_TIME, MAX_TILLED_TIME, cool=True)
                self.type = "tilled"
                player.hoe_durability -= TILLING_COST
                self.set_image()
            elif self.type == "dead" and player.fertilizer > 0:
                self.set_timer(MIN_REST_TIME, MAX_REST_TIME, cool=True)
                self.type = "resting"
                player.fertilizer -= 1
                self.set_image()

    def render(self, screen, cam):
        screen.blit(self.image, (self.pos - cam).to_int())
        if self.show_btn:
            screen.blit(Assets.get_image("btn_e"), (self.pos - cam + Vector2D(0, -16)).to_int())

