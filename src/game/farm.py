import pygame

from ..Net import Net
from ..utils import *
from ..objects import Player
from .menues import PauseMenu

class Farm:
    def __init__(self):
        self.player = Player(0, 0)
        self.pause_menue = PauseMenu()
        self.pause_menue_active = False

        self.running = True
        self.mouse_down = False

    def run(self):
        while self.running:
            self.update()
            self.render()
        Net.selected_slot = None

    def update(self):
        Net.click = False
        Net.dt = Net.clock.tick(Net.FPS)/1000.0
        Net.events = pygame.event.get()

        for event in Net.events:
            if event.type == pygame.QUIT:
                Net.shut_down()
            if event.type == pygame.MOUSEBUTTONDOWN: self.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP and self.mouse_down: 
                self.mouse_down = False
                Net.click = True

        if not self.pause_menue_active:
            self.player.update([])

        if self.pause_menue_active:
            code = self.pause_menue.update() 
            if code == "EXIT": self.running = False
            elif code == "CLOSE": self.pause_menue_active = False

        if Keys.is_pressed(Keys.escape): self.pause_menue_active = not self.pause_menue_active


    def render(self):
        Net.screen.fill((0, 0, 0))
        #render
        self.player.render()

        if self.pause_menue_active: self.pause_menue.render()
        #update
        pygame.display.flip()