import pygame

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def to_int(self): return (int(self.x), int(self.y))
    def to_tuple(self): return (tuple(self.x), tuple(self.y))

    def __add__(self, other):
        if type(other) == Vector2D:
            return Vector2D(self.x + other.x, self.y + other.y)
        else:
            return Vector2D(self.x + other, self.y + other)

    def __sub__(self, other):
        if type(other) == Vector2D:
            return Vector2D(self.x - other.x, self.y - other.y)
        else:
            return Vector2D(self.x - other, self.y - other)

    def __mul__(self, other):
        if type(other) == Vector2D:
            return Vector2D(self.x * other.x, self.y * other.y)
        else:
            return Vector2D(self.x * other, self.y * other)

    def __truediv__(self, other):
        if type(other) == Vector2D:
            return Vector2D(self.x / other.x, self.y / other.y)
        else:
            return Vector2D(self.x / other, self.y / other)


def on_cam(pos, dim, cam, screen_size):
    if pos.x + dim.x < cam.x: return False
    if pos.x > cam.x + screen_size.x: return False
    if pos.y + dim.y < cam.y: return False
    if pos.y > cam.y + screen_size.y: return False
    return True

