import pygame

from ..utils import Keys, Vector2D, Assets, AnimationManager, SubScreen


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
        self.inventory = PlayerInventory(self, screen)
        self.seeds = 5
        self.hoe_durability = 100
        self.fertilizer = 2
        self.plants = 0

    def rect(self):
        return pygame.Rect(self.pos.to_int(), (16, 16))

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

        self.inventory.render(screen, cam)

class PlayerInventory:
    def __init__(self, player: Player, screen: pygame.Surface):
        self.player = player
        self.image = Assets.get_image("inventory_ui")
        self.subscreen = SubScreen(0, 0, self.image.get_width(), self.image.get_height(), "black", screen)

    def update(self, dt, events):
        pass

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.subscreen.screen.blit(self.image, (0, 0))
        #update
        self.subscreen.render(cam)

