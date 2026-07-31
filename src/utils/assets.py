import pygame

from .animation import Animation

class _assets:
    def __init__(self):
        self.images: dict[str, pygame.Surface] = {}
        self.animations: dict[str, Animation] = {}
        self.fonts: dict[str, pygame.font.Font] = {}

    #clearing
    def _clear(self, _confirm=False):
        if _confirm:
            self.images = {}
            self.animations = {}
            self.fonts = {}

    def clear_images(self, _confirm=False):
        if _confirm:
            self.images = {}

    def del_image(self, name):
        if name in self.images:
            del self.images[name]

    def clear_animations(self, _confirm=False):
        if _confirm:
            self.animations = {}

    def del_animation(self, name):
        if name in self.animations:
            del self.animations[name]

    def clear_fonts(self, _confirm=False):
        if _confirm:
            self.fonts = {}

    def del_font(self, name):
        if name in self.fonts:
            del self.fonts[name]

    #creation
    def new_image(self, name, path, rect=None, scale=1.0, colorKey=(0, 0, 0), sWidth=None, sHeight=None):
        image = pygame.image.load(path)
        #rect
        if rect is not None:
            image = image.subsurface(rect)
        #scale
        if scale != 1.0:
            image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        #colorkey
        if colorKey is not None:
            image.set_colorkey(colorKey)
        #size
        if sWidth is not None and sHeight is not None:
            image = pygame.transform.scale(image, (sWidth, sHeight))
        self.images[name] = image.convert()

    def new_font(self, name, path, size):
        self.fonts[name] = pygame.font.Font(path, size)

    def new_animation(self, name, image, size=16, fps=3):
        self.animations[name] = Animation(image, size, fps)

    #getters
    def get_image(self, name):
        if name in self.images:
            return self.images[name]
        else:
            return None

    def get_animation(self, name):
        if name in self.animations:
            return self.animations[name]
        else:
            return None

    def get_font(self, name):
        if name in self.fonts:
            return self.fonts[name]
        else:
            return None

Assets = _assets()