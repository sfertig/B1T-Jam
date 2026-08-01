import asyncio
import pygame

from ..codes import *

from ..utils import Keys, Vector2D, Assets

from ..objects import Player, Tile

class Game_screen:
    def __init__(self, screen, clock):
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = clock

        self.return_code = None

        self.dt = 0.0

        self.p = Player(48, 160)

        self.cam = Vector2D(0, 0)

        self.test = Tile(192, 160, "tilled")

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

        if Keys.is_pressed(Keys.escape, events): self.return_code = SHUT_DOWN

        self.p.update(self.dt, events)
        self.test.update(self.dt, events, self.p)


    def render(self):
        #clear
        self.screen.fill(COLOR_1)
        self.screen.blit(Assets.get_image("game_bg"), (Vector2D(0, 0)-self.cam).to_int())
        #render
        self.test.render(self.screen, self.cam)
        self.p.render(self.screen, self.cam)
        #update
        pygame.display.flip()
