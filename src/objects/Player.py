import pygame

from ..utils import *


class Player:
    def __init__(self, x, y, screen, cam):
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

        #inventory / items
        self.seeds = 5
        self.max_seeds = 20
        self.hoe_durability = 100
        self.fertilizer = 2
        self.max_fertilizer = 5
        self.plants = 5
        self.max_plants = 15
        self.money = 100
        self.plants_to_money = 2

        self.inventory = PlayerInventory(self, screen, cam)

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


    def update(self, dt, events, rects: list[pygame.Rect]):
        self.manager.update(dt)
        self.inventory.update(dt, events)
        self.input(events)

        #x collisions
        self.pos.x += self.vel.x * dt
        for rect in rects:
            if self.rect().colliderect(rect):
                if self.vel.x > 0: #right
                    self.pos.x -= self.vel.x * dt
                    self.vel.x = 0
                elif self.vel.x < 0: #left
                    self.pos.x -= self.vel.x * dt
                    self.vel.x = 0
        #y collisions
        self.pos.y += self.vel.y * dt
        for rect in rects:
            if self.rect().colliderect(rect):
                if self.vel.y > 0: #down
                    self.pos.y -= self.vel.y * dt
                    self.vel.y = 0
                elif self.vel.y < 0: #up
                    self.pos.y -= self.vel.y * dt
                    self.vel.y = 0

        


    def render(self, screen, cam: Vector2D):
        image = self.manager.get_image()
        screen.blit(image, (self.pos - cam).to_int())

        self.inventory.render(screen, cam)

    #inventory funcs
    #-seeds
    def add_seeds(self, amount):
        self.seeds += amount
        if self.seeds > self.max_seeds: 
            self.seeds = self.max_seeds
            return False
        return True
    def take_seeds(self, amount):
        self.seeds -= amount
        if self.seeds < 0: 
            self.seeds = 0
            return False
        return True

    #-fertilizer
    def add_fertilizer(self, amount):
        self.fertilizer += amount
        if self.fertilizer > self.max_fertilizer: 
            self.fertilizer = self.max_fertilizer
            return False
        return True
    def take_fertilizer(self, amount):
        self.fertilizer -= amount
        if self.fertilizer < 0: 
            self.fertilizer = 0
            return False
        return True

    #-plants
    def add_plants(self, amount):
        num = self.plants
        self.plants += amount
        if self.plants > self.max_plants: 
            self.plants = num
            return False
        return True
    def take_plants(self, amount):
        self.plants -= amount
        if self.plants < 0: 
            self.plants = 0
            return False
        return True

    #-hoe
    def add_hoe_durability(self, amount):
        self.hoe_durability += amount
        print(self.hoe_durability)
        if self.hoe_durability > 100: 
            self.hoe_durability = 100
            return False
        return True
    def take_hoe_durability(self, amount):
        self.hoe_durability -= amount
        if self.hoe_durability < 0: 
            self.hoe_durability = 0
            return False
        return True

    #money
    def take_money(self, amount):
        num = self.money
        self.money -= amount
        if self.money < 0: 
            self.money = num
            return False
        return True


class PlayerInventory:
    def __init__(self, player: Player, screen: pygame.Surface, cam: Vector2D):
        self.player = player
        self.cam: Vector2D = cam
        self.image = Assets.get_image("inventory_ui")
        self.subscreen = SubScreen(0, 0, self.image.get_width(), self.image.get_height(), "black", screen)
        #ui ellements
        self.seed_bar = ProgressBar(10, 3, 9, 10, 0, self.player.max_seeds, self.player.seeds)
        self.fertilizer_bar = ProgressBar(80, 3, 9, 10, 0, self.player.max_fertilizer, self.player.fertilizer)
        self.plants_bar = ProgressBar(99, 3, 9, 10, 0, self.player.max_plants, self.player.plants)
        self.hoe_bar = ProgressBar(34, 10, 33, 1, 0, 100, self.player.hoe_durability)
        self.hunger = ProgressBar(13, 24, 86, 1, 0, 240, 240)
        self.hunger_timer = Timer(240)
        self.hunger_show_btn = False
        self.hunger_rect = pygame.Rect(16, 272, 32, 32)
        self.hunger_full = 240

        #set inital hunger wait
        self.hunger.value = self.hunger.max*1.25
        self.hunger_full = self.hunger.value
        self.hunger_timer = Timer(self.hunger_full)

    def handle_hunger(self, events):
        if self.cam.to_int() == (0, 0):
            if self.player.rect().colliderect(self.hunger_rect) and (self.hunger.value < self.hunger.max):
                self.hunger_show_btn = True
                if Keys.is_pressed(Keys.e, events) and self.player.take_plants(1): 
                    self.hunger.value = self.hunger.max*1.25
                    self.hunger_full = self.hunger.value
                    self.hunger_timer = Timer(self.hunger_full)
            else:
                self.hunger_show_btn = False


    def update(self, dt, events):
        self.seed_bar.update(self.player.seeds)
        self.fertilizer_bar.update(self.player.fertilizer)
        self.plants_bar.update(self.player.plants)
        self.hoe_bar.update(self.player.hoe_durability)

        self.handle_hunger(events)
        self.hunger_timer.update(dt)
        self.hunger.update(int(self.hunger_full - self.hunger_timer.get_time()))

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.subscreen.screen.blit(self.image, (0, 0))
        self.seed_bar.render(self.subscreen.screen, Vector2D(0, 0))
        self.fertilizer_bar.render(self.subscreen.screen, Vector2D(0, 0))
        self.plants_bar.render(self.subscreen.screen, Vector2D(0, 0))
        self.hoe_bar.render(self.subscreen.screen, Vector2D(0, 0))
        self.hunger.render(self.subscreen.screen, Vector2D(0, 0))
        if self.hunger_show_btn:
            screen.blit(Assets.get_image("btn_e"), (24, 248))
        #update
        self.subscreen.render(cam)

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


