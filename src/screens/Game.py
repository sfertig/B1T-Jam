import asyncio
import pygame
import random

from ..codes import *

from ..utils import Keys, Vector2D, Assets, Timer, Sound
from ..objects.dayManager import SLEEP_WIDTH

from ..objects import *

NIGHT_TIME = 6

DIFFICULTY = 100

def gen_collisions():
    return [
    ]

class Game_screen:
    def __init__(self, screen, clock):
        self.screen: pygame.Surface = screen
        self.clock: pygame.time.Clock = clock
        self.collisions = gen_collisions()

        self.day_manager = DayManager(self.screen)

        self.return_code = None

        self.dt = 0.0
        self.cam = Vector2D(-50, 0)

        self.p: Player = Player(48, 160, self.screen, self.cam)
        
        self.house = House(self.screen, self.cam)

        self.tile_manager = TileManager()

        self.paused = False
        self.death = False
        self.speed = False
        self.pause_menu = PauseMenu(self.screen)
        self.death_menu = DeathMenu(self.screen)

        self.sound = Sound(Assets.get_sound("bg_music"), 100, -1)
        self.sound.play()

    def update_cam(self):
        if self.p.pos.x < 0:
            self.cam.x = -370
        else:
            self.cam.x = 0

    def detect_death(self):
        if self.day_manager.bar.value >= self.day_manager.bar.max: self.death = True
    async def detect_sleep(self, events):
        if self.house.bed_show_e:
            if Keys.is_pressed(Keys.e, events):
                if self.day_manager.bar.rect().width > SLEEP_WIDTH: 
                    await self.sleep_reset()

    def handle_hunger(self):
        if self.p.inventory.hunger_timer.is_done(): self.death = True


    async def sleep_reset(self):
        global DIFFICULTY
        DIFFICULTY-=10
        DIFFICULTY = max(DIFFICULTY, 3)
        self.day_manager.sleep()
        #other night time things
        timer = Timer(NIGHT_TIME)
        self.tile_manager.sleep(DIFFICULTY)
        while not timer.is_done():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.return_code =  SHUT_DOWN
                    break
            self.dt = self.clock.tick(FPS)/1000.0
            timer.update(self.dt)
            #render stuff
            self.screen.blit(Assets.get_image("sleep_ui"), (0, 0))
            pygame.display.flip()

            await asyncio.sleep(0)
        #you wake back up



    async def run(self):
        self.return_code = None
        while True:
            if self.return_code is not None:
                self.sound.stop()
                return self.return_code
            
            await self.update()
            self.render()
            await asyncio.sleep(0)

    async def update(self):
        self.dt = self.clock.tick(FPS)/1000.0

        events = pygame.event.get().copy()

        for event in events:
            if event.type == pygame.QUIT:
                self.return_code =  SHUT_DOWN

        if Keys.is_pressed(Keys.escape, events) and not self.death:
            self.paused = not self.paused
            self.pause_menu.active = self.paused

        if not self.paused:
            self.day_manager.update(self.dt, events, self.p)
            self.detect_death()
            self.p.update(self.dt, events, self.collisions)
            self.tile_manager.update(self.dt, events, self.p)
            self.house.update(self.dt, events, self.p)
            self.handle_hunger()
        elif self.paused:
            num = self.pause_menu.update(self.dt, events)
            if num is not None:
                self.return_code = num
            else:
                self.paused = self.pause_menu.active
        if self.death: 
            self.death_menu.update(self.dt, events)
            if not self.death_menu.active:
                self.return_code = TITLE_SCREEN

        await self.detect_sleep(events)



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
        elif self.death:
            self.death_menu.render()

        #update
        pygame.display.flip()
