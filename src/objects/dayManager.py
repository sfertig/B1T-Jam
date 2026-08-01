import pygame

from .Player import ProgressBar, Player

from ..utils import Vector2D, Assets, Keys, Timer, SubScreen

DAY_LENGTH = 120 #seconds

class DayManager:
    def __init__(self, screen):
        self.day = 1
        self.bar = ProgressBar(14, 7, 53, 2, 0, DAY_LENGTH, 0)
        self.subscreen = SubScreen(128, 0, 80, 16, "black", screen)
        self.screen = self.subscreen.screen
        self.timer = Timer(DAY_LENGTH)

    def update(self, dt, events, player):
        self.timer.update(dt)

        self.bar.update(int(self.timer.get_time()))

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.screen.blit(Assets.get_image("day_ui"), (0, 0))
        self.bar.render(self.screen, Vector2D(0, 0))
        #update
        self.subscreen.render(cam)

class House:
    def __init__(self, screen, cam):
        self.image = Assets.get_image("house")
        self.subscreen = SubScreen(-80, 0, 80, 352, "black", screen)
        self.screen = self.subscreen.screen
        self.workbench_rect = pygame.Rect(17, 35, 43, 11)
        self.show_workbench_btn = False
        self.shop = Shop(screen, cam)
        self.cam: Vector2D = cam

    def update(self, dt, events, player):
        r = self.subscreen.get_global_rect(self.workbench_rect.copy())
        if r.colliderect(player.rect()):
            self.show_workbench_btn = True
            self.cam.y = -110
        else:
            self.show_workbench_btn = False
            self.cam.y = 0

        if self.show_workbench_btn:
            self.shop.update(dt, events, player)
        

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.screen.blit(self.image, (0, 0))
        if self.show_workbench_btn:
            self.shop.render(screen, cam)
        #update
        self.subscreen.render(cam)

class Shop:
    def __init__(self, screen, cam):
        self.image = Assets.get_image("shop")
        self.subscreen = SubScreen(-368, -105, 368, 100, "black", screen)
        self.screen = self.subscreen.screen
        self.seeds_rect = pygame.Rect(16, 16, 32, 16)
        self.hoe_rect = pygame.Rect(16, 38, 32, 16)
        self.mouse_down = False
        self.cam: Vector2D = cam

    def handle_seeds(self, player: Player):
        if self.seeds_rect.collidepoint(self.subscreen.local_mouse_pos(self.cam).to_int()) and player.seeds < player.max_seeds:
            if player.take_plants(1): 
                player.add_seeds(player.max_seeds)
    def handle_hoe(self, player: Player):
        if self.hoe_rect.collidepoint(self.subscreen.local_mouse_pos(self.cam).to_int()) and player.hoe_durability < 100:
            if player.take_plants(1): 
                player.add_hoe_durability(100)


    def update(self, dt, events, player):
        click = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
                click = True
                self.mouse_down = False

        if click:
            self.handle_seeds(player)
            self.handle_hoe(player)

    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.screen.blit(self.image, (0, 0))

        #update
        self.subscreen.render(cam)

