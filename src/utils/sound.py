import pygame

from .assets import Assets

class Sound:
    def __init__(self, sound: pygame.mixer.Sound, volume: int, loop: int=0):
        self.sound = sound
        self.volume = volume
        self.loop = loop

    def play(self):
        #only play if not already playing
        if not self.is_done():
            return
        self.sound.set_volume(self.volume / 100.0)
        self.sound.play(loops=self.loop)


    def stop(self):
        self.sound.stop()

    def toggle(self):
        if self.playing:
            self.stop()
        else:
            self.play()

    def is_done(self):
        return True

class SoundManager:
    def __init__(self, sounds: dict[str, Sound], current_sound=None):
        self.sounds = sounds
        self.current_sound = current_sound

    def new_sound(self, name, volume=100, loop=0):
        self.sounds[name] = Sound(Assets.get_sound(name), volume, loop)

    def play(self, name):
        self.sounds[name].play()
        self.current_sound = name

    def stop(self, name=None):
        if name is not None:
            self.sounds[name].stop()
            return
        self.sounds[self.current_sound].stop()
        self.current_sound = None

