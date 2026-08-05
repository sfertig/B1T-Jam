import pygame
import json

def save_json(data, path)
    d = {}
    for k, v in data.items():
        d[str(k[0])+";"+str(k[1])] = v

    with open(path, 'w') as file:
        json.dump(data, file)

def load_json(path):
    d = {}
    data = {}
    with open(path, 'r') as file:
        d = json.read(file)
    for k,v in d.items():
        #TODO: add key decoding
        pass

    return data



class Collisions:
    def __init__(self, data: dict):
        self.tiles = data

    def load(path):
        self.tiles = load_json(path)

    def save(self path):
        save_json(self.tiles, path)
