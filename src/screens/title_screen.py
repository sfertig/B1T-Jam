import pygame
import sys
from ..Net import Net
from ..utils import Assets, Keys, save_settings, Vector2D, SubScreen, save_all_saves

FPS = 60

def Title_Image(self):
    while True:
        # -- update --
        Net.events = pygame.event.get().copy()
        for event in Net.events:
            if event.type == pygame.QUIT:
                self.shut_down()
        if Keys.is_pressed(Keys.escape): Net.shut_down()
        elif Keys.is_pressed(Keys.enter) or pygame.mouse.get_pressed()[0]: break
        # -- render --
        Net.screen.fill("green")
        #render

        #update
        pygame.display.flip()




class Title_screen:
    def __init__(self):
        self.bg = "black"
        self.slot_1 = save_slot(1, Vector2D(143, 95))
        self.slot_2 = save_slot(2, Vector2D(271, 95))
        self.slot_3 = save_slot(3, Vector2D(399, 95))
        self.slots = [self.slot_1, self.slot_2, self.slot_3]

    def run(self):
        #Title_Image()
        while True:
            self.update()
            self.render()

    def update(self):
        Net.dt = Net.clock.tick(FPS)/1000.0

        Net.events = pygame.event.get().copy()

        for event in Net.events:
            if event.type == pygame.QUIT:
                self.shut_down()

        if Keys.is_pressed(Keys.escape): Net.shut_down()

        for slot in self.slots: slot.update()


    def render(self):
        #clear
        Net.screen.fill(self.bg)
        #render
        for slot in self.slots: slot.render()
        #update
        pygame.display.flip()


class save_slot:
    def __init__(self, num, pos: Vector2D):
        self.num = num
        self.pos = pos
        self.data = getattr(Net, f"slot_{num}")
        self.outline = Assets.get_image("save_slot_outline")
        dim = self.outline.get_size()
        self.subscreen = SubScreen(pos.x, pos.y, dim[0], dim[1], "black", Net.screen)
        self.screen = self.subscreen.screen
        self.empty = not self.data["created"]
        self.hovered = False
        self.created = self.data["created"]

    def update(self):
        self.hovered = False
        rect = self.subscreen.get_global_rect(self.screen.get_rect())
        if rect.collidepoint(pygame.mouse.get_pos()): self.hovered = True
        if self.hovered and pygame.mouse.get_pressed()[0] and not self.created: 
            self.data["created"] = True
            self.empty = False
            self.created = True
        

    def render(self):
        self.subscreen.clear()
        #render
        self.screen.blit(self.outline, (0, 0))
        #empty
        if self.empty and not self.hovered:
            self.screen.blit(Assets.get_image("save_slot_empty"), (16, 48))
        elif self.hovered and self.empty:
            self.screen.blit(Assets.get_image("save_slot_create"), (16, 48))
        elif self.created and self.hovered:
            self.screen.blit(Assets.get_image("save_slot_play"), (16, 96))

        #update
        self.subscreen.render(Net.cam)

