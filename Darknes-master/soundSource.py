import pygame
from sound import Sound

class Source:
    def __init__(self, loc, file, interval, lifespan=1500, res=64, color = (255,255,255)):
        self.loc = loc
        self.voice = pygame.mixer.Sound(file) if file else None
        self.interval = interval
        self.lifespan = lifespan
        self.sounds = []
        self.clock = 0
        self.res = res
        self.color = color

    def update(self, level, block_size):
        self.clock += 1
        if self.clock in [self.interval, self.interval-3]:
            self.sounds.append(Sound(self.loc, self.lifespan, res=self.res, color=self.color))
        if self.clock == self.interval:
            if self.voice != None:
                self.voice.play(maxtime=self.lifespan, fade_ms=self.lifespan//4)
            self.clock = 0
        for s in self.sounds:
            if s.update(level, block_size):
                self.sounds.remove(s)

        return None

    def draw(self, screen):
        for s in self.sounds:
            s.draw(screen)
