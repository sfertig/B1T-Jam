import pygame
import json

from .input import Keys
from .math import Vector2D

def save_json(data, path):
    d = {}
    for k, v in data.items():
        d[str(str(k[0])+";"+str(k[1]))] = v

    with open(path, 'w') as file:
        json.dump(d, file)

def load_json(path):
    d = {}
    data = {}
    with open(path, 'r') as file:
        d = json.load(file)
    for k,v in d.items():
        k = k.split(";")
        data[(int(k[0]), int(k[1]))] = v

    return data



class Collisions:
    def __init__(self, data: dict = {}, build=True):
        self.tiles = {}
        for k,v in data.items():
            k = k.split(";")
            self.tiles[(int(k[0]), int(k[1]))] = v
        self.active = False
        self.build = build

    def load(self, path):
        self.tiles = load_json(path)

    def save(self, path):
        if self.build: return
        save_json(self.tiles, path)

    def update(self, events, cam: Vector2D):
        if self.build: return
        if Keys.is_pressed(Keys.c, events): self.active = not self.active
        if not self.active: return

        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] or mouse_buttons[2]:
            mpos = pygame.mouse.get_pos()
            world_x = int((mpos[0] + cam.x) // 16) * 16
            world_y = int((mpos[1] + cam.y) // 16) * 16
            tile_pos = (world_x, world_y)
            if mouse_buttons[0]:
                self.tiles[tile_pos] = 1
            elif mouse_buttons[2]:
                self.tiles.pop(tile_pos, None)
            

    def get_tiles(self):
        rects = []
        for pos, value in self.tiles.items():
            x, y = pos
            rect = pygame.Rect(x, y, 16, 16)
            rects.append(rect)
        return rects

    def render(self, screen, cam):
        if self.build: return
        if self.active:
            for pos, value in self.tiles.items():
                x, y = pos
                rect = pygame.Rect(x-cam.x, y-cam.y, 16, 16)
                pygame.draw.rect(screen, "yellow", rect, 1)
            #render tile to mpos but aligned to grid
            mpos = pygame.mouse.get_pos()
            mpos = ((mpos[0]//16)*16, (mpos[1]//16)*16)
            rect = pygame.Rect(mpos[0], mpos[1], 16, 16)
            pygame.draw.rect(screen, "yellow", rect, 1)
