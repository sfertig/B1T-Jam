import pygame
import sys
from ..Net import Net

from ..utils import Assets, Keys, save_settings

FPS = 60

class Title_Image:
    def run(self):
        while True:
            num = self.update()
            self.render()
            if num != 0: break

    def update(self):
        Net.dt = Net.clock.tick(FPS)/1000.0

        Net.events = pygame.event.get().copy()

        for event in Net.events:
            if event.type == pygame.QUIT:
                self.shut_down()

        if Keys.is_pressed(Keys.escape): shut_down()
        elif Keys.is_pressed(Keys.enter) or pygame.mouse.get_pressed()[0]: return 1

        return 0

    def render(self):
        #clear
        Net.screen.fill("green")
        #render

        #update
        pygame.display.flip()

class Title_screen:
    def __init__(self):
        self.bg = "black"

    def run(self):
        #Title_Image().run()
        while True:
            self.update()
            self.render()

    def update(self):
        Net.dt = Net.clock.tick(FPS)/1000.0

        Net.events = pygame.event.get().copy()

        for event in Net.events:
            if event.type == pygame.QUIT:
                self.shut_down()

        if Keys.is_pressed(Keys.escape): shut_down()


    def render(self):
        #clear
        Net.screen.blit(Assets.get_image("save_slot_bg"), (0, 0))
        #render

        #update
        pygame.display.flip()

def shut_down():
    #save
    save_settings(Net.settings)
    #exit
    pygame.quit()
    sys.exit()

