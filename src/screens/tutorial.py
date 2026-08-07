import asyncio
import pygame

from ..codes import *

from ..utils import Keys, Vector2D, Assets

class Tutorial:
    def __init__(self, screen, clock):
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = clock

        self.return_code = None

        self.dt = 0.0


    async def run(self):
        self.return_code = None
        while True:
            if self.return_code is not None:
                return self.return_code
            
            self.update()
            self.render()
            await asyncio.sleep(0)

    def update(self):
        self.dt = self.clock.tick(FPS)/1000.0

        events = pygame.event.get().copy()

        for event in events:
            if event.type == pygame.QUIT:
                self.return_code =  SHUT_DOWN

        if Keys.is_pressed(Keys.escape, events): self.return_code = TITLE_SCREEN
        elif Keys.is_pressed(Keys.enter, events): self.return_code = GAME_SCREEN


    def render(self):
        #clear
        self.screen.blit(Assets.get_image("tutorial"), (0, 0))

        #render
        #update
        pygame.display.flip()
