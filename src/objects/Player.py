import pygame

from ..utils import Keys, Vector2D, Assets, AnimationManager, SubScreen, Text


class Player:
    def __init__(self, x, y, screen):
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
        self.max_seeds = 10
        self.hoe_durability = 100
        self.fertilizer = 2
        self.max_fertilizer = 5
        self.plants = 0
        self.max_plants = 10

        self.inventory = PlayerInventory(self, screen)

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


    def update(self, dt, events):
        self.manager.update(dt)
        self.inventory.update(dt, events)
        self.input(events)

        self.pos += (self.vel*dt)
        #TODO: add collision


    def render(self, screen, cam: Vector2D):
        image = self.manager.get_image()

        screen.blit(image, (self.pos - cam).to_int())

        pygame.draw.rect(screen, (255, 0, 0), self.rect(), 1) #debug

        self.inventory.render(screen, cam)

class PlayerInventory:
    def __init__(self, player: Player, screen: pygame.Surface):
        self.player = player
        self.image = Assets.get_image("inventory_ui")
        self.subscreen = SubScreen(0, 0, self.image.get_width(), self.image.get_height(), "black", screen)
        #ui ellements
        self.seed_bar = ProgressBar(10, 3, 9, 10, 0, self.player.max_seeds, self.player.seeds)
        self.fertilizer_bar = ProgressBar(80, 3, 9, 10, 0, self.player.max_fertilizer, self.player.fertilizer)
        self.plants_bar = ProgressBar(99, 3, 9, 10, 0, self.player.max_plants, self.player.plants)
        self.hoe_bar = ProgressBar(34, 10, 33, 1, 0, 100, self.player.hoe_durability)

    def update(self, dt, events):
        self.seed_bar.update(self.player.seeds)
        self.fertilizer_bar.update(self.player.fertilizer)
        self.plants_bar.update(self.player.plants)
        self.hoe_bar.update(self.player.hoe_durability)

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.subscreen.screen.blit(self.image, (0, 0))
        self.seed_bar.render(self.subscreen.screen, Vector2D(0, 0))
        self.fertilizer_bar.render(self.subscreen.screen, Vector2D(0, 0))
        self.plants_bar.render(self.subscreen.screen, Vector2D(0, 0))
        self.hoe_bar.render(self.subscreen.screen, Vector2D(0, 0))
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
        return pygame.Rect(self.pos.to_int(), (rel_width, self.dim.y))

    def update(self, value):
        self.value = value

    def render(self, screen, cam: Vector2D):
        r = self.rect()
        r.topleft = (self.pos - cam).to_int()
        pygame.draw.rect(screen, (255, 255, 255), r)

