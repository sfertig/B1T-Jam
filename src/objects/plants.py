import pygame
import random
from ..utils import *
from ..Net import Net

class Plant:
    def __init__(self, x, y, type, state="resting"):
        self.pos = Vector2D(x, y)
        self.type = type
        self.state = state

    def get_image(self):
        if self.state == "none": return Assets.get_image("pt_none")
        return Assets.get_image("pt_" + self.type + "_" + self.state)

    def update(self):
        pass

    def render(self):
        image = self.get_image()
        Net.screen.blit(image, (self.pos - Net.cam).to_int())

class PlantManager:
    def __init__(self):
        self.plants: list[Plant] = []

    def save_data(self, data):
        d = {}
        for plant in self.plants:
            d[str(plant.pos.x) + ";" + str(plant.pos.y)] = {"type": plant.type, "state": plant.state}

        data["plant_data"] = d

    def load_data(self, data):
        for k, v, in data["plant_data"].items():
            pos = k.split(";")
            self.plants.append(Plant(int(pos[0]), int(pos[1]), v["type"], v["state"]))
        # -- if no plants then a new save was just started --
        if len(self.plants) == 0:
            for y in range(32, 320, 16):
                for x in range(144, 576, 16):
                    self.plants.append(Plant(x, y, "wheat", "none"))
        for i in range(5):
            p = random.choice(self.plants)
            p.state = "resting"
    def update(self):
        for plant in self.plants:
            plant.update()

    def render(self):
        for plant in self.plants:
            plant.render()

