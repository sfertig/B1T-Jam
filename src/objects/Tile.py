import pygame
import random

from ..utils import *
from .Player import Player

TILLING_COST = 10
MIN_TILLING_COST = 1
DEAD_COST = 1

MIN_GROW_TIME = 20
MAX_GROW_TIME = 45

MIN_REST_TIME = 20
MAX_REST_TIME = 45

MIN_TILLED_TIME = 20
MAX_TILLED_TIME = 45

MIN_DEATH_TIME = 20 #TODO: add return to death state in night time
MAX_DEATH_TIME = 45

class Tile:
    def __init__(self, x, y, type, sound: SoundManager):
        self.pos = Vector2D(x, y)
        self.type = type
        self.image = None
        self.rect = pygame.Rect((x, y), (16, 16))
        if self.type not in ["dead", "resting", "tilled", "growing", "grown", "none"]:
            raise ValueError(f"Invalid tile type: {self.type}")

        self.set_image()
        self.show_btn = False
        self.sound: SoundManager = sound

        self.timer = Timer(random.randint(MIN_GROW_TIME, MAX_GROW_TIME))
        self.timer.elapsed = self.timer.duration #set inital hilight
        self.cooldown = False

    def set_image(self):
        self.image = Assets.get_image(f"tile_{self.type}")
    def set_show_btn(self, player):
        if self.type in ["tilled", "resting", "grown", "dead"] and player.rect().colliderect(self.rect) and not self.cooldown:self.show_btn = True
        else: self.show_btn = False
        #check if player has needed items to interact with tile
        if self.show_btn:
            if self.type == "tilled" and player.seeds <= 0: self.show_btn = False
            elif self.type == "resting" and player.hoe_durability <= 0: self.show_btn = False
            elif self.type == "dead" and player.fertilizer <= 0: self.show_btn = False

    def set_timer(self, min=MIN_GROW_TIME, max=MAX_GROW_TIME, cool=False):
        self.timer = Timer(random.randint(min, max))
        self.cooldown = cool

    def set_type(self, type):
        if type not in ["dead", "resting", "tilled", "growing", "grown", "none"]:
            raise ValueError(f"Invalid tile type: {type}")
        self.type = type
        self.set_image()

    def is_active(self):
        #return is can be currently interacted with
        if self.type == "grown": return True
        if self.type in ["dead", "resting", "tilled", "dead"]: return self.timer.is_done()


    def update(self, dt, events, player: Player):

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

        if self.show_btn and (Keys.is_pressed(Keys.e, events) or Keys.is_pressed(Keys.space, events)):
            self.sound.play("tile")
            if self.type == "tilled" and player.take_seeds(1):
                self.type = "growing"
                self.set_image()
                player.seeds -= 1
                self.set_timer()
            elif self.type == "grown" and player.add_plants(1):
                self.set_timer(MIN_REST_TIME, MAX_REST_TIME, cool=True)
                self.type = "resting"
                self.set_image()
            elif self.type == "resting" and player.hoe_durability > 0 and player.take_hoe_durability(TILLING_COST):
                self.set_timer(MIN_TILLED_TIME, MAX_TILLED_TIME, cool=True)
                self.type = "tilled"
                self.set_image()
            elif self.type == "dead" and player.fertilizer > 0 and player.take_fertilizer(DEAD_COST):
                self.set_timer(MIN_REST_TIME, MAX_REST_TIME, cool=True)
                self.type = "resting"
                self.set_image()

    def render(self, screen, cam):
        screen.blit(self.image, (self.pos - cam).to_int())

        if self.is_active():
            r = self.rect.copy()
            r.topleft = (self.pos - cam).to_int()
            pygame.draw.rect(screen, (255, 255, 255), r, 1)
        
        if self.show_btn:
            screen.blit(Assets.get_image("btn_e"), (self.pos - cam + Vector2D(0, -16)).to_int())


MIN_NEW_TIME = 20
MAX_NEW_TIME = 60


class TileManager:
    def __init__(self):
        self.tiles: list[Tile] = []
        self.sound: SoundManager = SoundManager({"tile": Sound(Assets.get_sound("tile"), 5)})
        for y in range(32, 320, 16):
            for x in range(144, 576, 16):
                self.tiles.append(Tile(x, y, "none", self.sound))
        self.none = self.tiles.copy()
        while True:
            tile = random.choice(self.tiles)
            if tile.pos.x == 144: break
            
        tile.set_type("resting")
        self.none.remove(tile)
        for i in range(50):
            self.get_new_tile()
        self.timer = Timer(random.randint(MIN_NEW_TIME, MAX_NEW_TIME))


    def get_type(self):
        #return mainly resting, but sometimes dead
        return random.choice(["resting", "dead", "resting", "resting", "resting", "resting", "resting"])

    def sleep(self, dificulty: int):
            for tile in self.tiles:
                if tile.type == "none": continue
                if tile.type != "grown":
                    if random.randint(0, dificulty) == 0:
                        tile.set_type("dead")
                    else:
                        if random.randint(0, dificulty*2) == 0:
                            tile.set_type("dead")

    def get_new_tile(self):
        valid_candidates = []

        for tile in self.none:
            px, py = tile.pos.x, tile.pos.y
            for _t in self.tiles:
                if _t.type != "none":
                    is_neighbor = ((abs(_t.pos.x - px) == 16 and _t.pos.y == py) or
                        (abs(_t.pos.y - py) == 16 and _t.pos.x == px))
                    if is_neighbor:
                        valid_candidates.append(tile)
                        break  

        if valid_candidates:
            tile = random.choice(valid_candidates)
            tile.set_type(self.get_type())
            self.none.remove(tile)
        

    def update(self, dt, events, player):
        if self.timer.update(dt) and len(self.none) > 0:
            self.get_new_tile()
            self.timer = Timer(random.randint(MIN_NEW_TIME, MAX_NEW_TIME))

        for tile in self.tiles:
            tile.update(dt, events, player)

    def render(self, screen, cam):
        for tile in self.tiles:
            tile.render(screen, cam)

