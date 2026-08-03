import pygame

from .assets import Assets

class Sound:
    def __init__(self, sound: pygame.mixer.Sound, volume: int, loop: int):
        self.sound = sound
        self.volume = volume
        self.loop = loop

        self.playing = False

    def play(self):
        self.sound.set_volume(self.volume / 100.0)
        self.sound.play(loops=self.loop)
        self.playing = True

    def stop(self):
        self.sound.stop()
        self.playing = False

    def toggle(self):
        if self.playing:
            self.stop()
        else:
            self.play()

class SoundManager:
    def __init__(self, sounds: dict[str, Sound], current_sound=None):
        self.sounds = sounds
        self.current_sound = current_sound

    def new_sound(self, name, volume=100, loop=0):
        self.sounds[name] = Sound(Assets.get_sound(name), volume, loop)

    def play(self, name):
        self.sounds[name].play()
        self.current_sound = name

    def stop(self):
        self.sounds[self.current_sound].stop()
        self.current_sound = None

