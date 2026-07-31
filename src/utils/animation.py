import pygame

class Animation:
    def __init__(self, image: pygame.Surface, size: int, fps: float):
        self.image = image
        self.size = size
        self.fps = fps
        self.images = []
        self.index = 0.0

        # Automatically calculate frames based on image width
        total_frames = image.get_width() // size
        
        for i in range(total_frames):
            # Slice each frame from the sheet
            frame_rect = pygame.Rect(i * size, 0, size, size)
            self.images.append(self.image.subsurface(frame_rect))

    def update(self, dt: float):
        self.index += self.fps * dt
        self.index %= len(self.images)

    def flip_v(self):
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.flip(self.images[i], False, True)

    def flip_h(self):
        for i in range(len(self.images)):
            self.images[i] = pygame.transform.flip(self.images[i], True, False)

    def get_image(self):
        return self.images[int(self.index)]

    def copy(self):
        return Animation(self.image, self.size, self.fps)

class AnimationManager:
    def __init__(self, animations: dict[str, Animation], current_anim=None):
        self.animations = animations
        self.current_anim = current_anim
        print(self.animations)

    def new_anim(self, name, anim):
        self.animations[name] = anim

    def new_anim_set(self, anims: dict[str, Animation]):
        #add new anims to existing ones
        self.animations.update(anims)

    def flip_v(self):
        for name in self.animations:
            self.animations[name].flip_v()

    def flip_h(self):
        for name in self.animations:
            self.animations[name].flip_h()

    def change_anim(self, name):
        self.current_anim = name

    def update(self, dt: float):
        if self.current_anim is None and self.current_anim in self.animations:
            return
        self.animations[self.current_anim].update(dt)
    def get_image(self):
        if self.current_anim is None and self.current_anim in self.animations:
            return
        return self.animations[self.current_anim].get_image()

class Text:
    def __init__(self, font, text, color, size, x, y):
        self.font = font
        self.text = text
        self.color = color
        self.size = size
        self.x = x
        self.y = y

    def render(self, screen):
        text = self.font.render(self.text, True, self.color)
        text_rect = text.get_rect(topleft=(self.x, self.y))
        screen.blit(text, text_rect)
