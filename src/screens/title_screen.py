import asyncio
import pygame

from ..codes import *

class Title_screen:
    def __init__(self, screen, clock):
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = clock

        self.return_code = None

        self.dt = 0.0

    async def run(self):
        while True:
            if self.return_code is not None:
                return self.return_code
            
            self.update()
            self.render()
            asyncio.sleep(0)

    def update(self):
        self.dt = self.clock.tick(FPS)

        events = pygame.event.get().copy()

        for event in events:
            if event.type == pygame.QUIT:
                self.return_code =  SHUT_DOWN

    def render(self):
        #cleear
        self.screen.fill((0, 0, 0)) # TODO: remove for final colors

        #render

        #update
