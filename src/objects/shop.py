import pygame

from ..utils import *
from .Player import ProgressBar, Player
from .Tile import TILLING_COST, MIN_TILLING_COST


class Shop:
    def __init__(self, screen, cam):
        self.image = Assets.get_image("shop")
        self.subscreen = SubScreen(-370, 5, 272, 350, "black", screen)
        self.screen = self.subscreen.screen
        self.seeds_rect = pygame.Rect(16, 16, 32, 16)
        self.hoe_rect = pygame.Rect(112, 16, 32, 16)
        self.fertaliser_rect = pygame.Rect(64, 16, 32, 16)
        self.mouse_down = False
        self.cam: Vector2D = cam
        self.upgrade_hoe_rect = pygame.Rect(16, 48, 32, 16)
        self.sell_rect = pygame.Rect(229, 32, 32, 16)

        self.money_bar = ProgressBar(71, 305, 176, 3, 0, 500, 0)

    def handle_shop(self, player: Player):
        global TILLING_COST
        global MIN_TILLING_COST

        if self.seeds_rect.collidepoint(self.subscreen.local_mouse_pos(self.cam).to_int()) and player.seeds < player.max_seeds:
            if player.take_money(2): 
                player.add_seeds(player.max_seeds)

        if self.hoe_rect.collidepoint(self.subscreen.local_mouse_pos(self.cam).to_int()) and player.hoe_durability < 100:
            if player.take_money(2): 
                player.add_hoe_durability(100)

        if self.fertaliser_rect.collidepoint(self.subscreen.local_mouse_pos(self.cam).to_int()) and player.fertilizer < player.max_fertilizer:
            if player.take_money(2): 
                player.add_fertilizer(player.max_fertilizer)

        if self.upgrade_hoe_rect.collidepoint(self.subscreen.local_mouse_pos(self.cam).to_int()):
            if player.take_money(5): 
                TILLING_COST -=1
                TILLING_COST = max(MIN_TILLING_COST, TILLING_COST)

        if self.sell_rect.collidepoint(self.subscreen.local_mouse_pos(self.cam).to_int()):
            if player.take_plants(1): 
                player.money += player.plants_to_money


    def update(self, dt, events, player):
        click = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: 
                click = True
                self.mouse_down = False

        if click: self.handle_shop(player)
        self.money_bar.update(player.money)


    def render(self, screen, cam: Vector2D):
        self.subscreen.clear()
        #render
        self.screen.blit(self.image, (0, 0))
        self.money_bar.render(self.screen, Vector2D(0, 0))

        #update
        self.subscreen.render(cam)

