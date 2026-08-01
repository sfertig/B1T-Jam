import asyncio
import pygame

from ..codes import *

from ..utils import Keys, Vector2D, Assets

from ..objects import *

class Game_screen:
    def __init__(self, screen, clock):
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = clock

        self.day_manager = DayManager(self.screen)

        self.return_code = None

        self.dt = 0.0

        self.p = Player(48, 160, self.screen)

        self.cam = Vector2D(-50, 0)
        self.house = House(self.screen, self.cam)

        self.tile_manager = TileManager()

        self.paused = False
        self.pause_menu = PauseMenu(self.screen)

    def update_cam(self):
        if self.p.pos.x < 0:
            self.cam.x = -370
        else:
            self.cam.x = 0


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

        if Keys.is_pressed(Keys.escape, events):
            self.paused = not self.paused
            self.pause_menu.active = self.paused

        if not self.paused:
            self.day_manager.update(self.dt, events)
            self.p.update(self.dt, events)
            self.tile_manager.update(self.dt, events, self.p)
            self.house.update(self.dt, events, self.p)
        else:
            num = self.pause_menu.update(self.dt, events)
            if num is not None:
                self.return_code = num
            else:
                self.paused = self.pause_menu.active


    def render(self):
        self.update_cam()
        #clear
        self.screen.fill(COLOR_1)
        self.screen.blit(Assets.get_image("game_bg"), (Vector2D(0, 0)-self.cam).to_int())
        #render
        self.house.render(self.screen, self.cam)
        self.tile_manager.render(self.screen, self.cam)
        self.day_manager.render(self.screen, self.cam)
        self.p.render(self.screen, self.cam)

        if self.paused:
            self.pause_menu.render()

        #update
        pygame.display.flip()
