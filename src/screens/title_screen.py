import pygame
import sys
from ..Net import Net

from ..utils import Assets, Keys

FPS = 60

class Title_screen:
    def __init__(self):
        self.bg = "black"

    def run(self):
        while True:
            self.update()
            self.render()

    def update(self):
        Net.dt = Net.clock.tick(FPS)/1000.0

        Net.events = pygame.event.get().copy()

        for event in Net.events:
            if event.type == pygame.QUIT:
                self.shut_down()

        if Keys.is_pressed(Keys.escape): self.shut_down()


    def render(self):
        #clear
        Net.screen.fill(self.bg)
        #render

        #update
        pygame.display.flip()

    def shut_down(self):
        pygame.quit()
        sys.exit()

