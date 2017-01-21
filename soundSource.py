import pygame
from sound import Sound

class Source:
    def __init__(self, loc, file, interval, lifespan=1500):
        self.loc = loc
        self.voice = pygame.mixer.Sound(file)
        self.interval = interval
        self.lifespan = lifespan
        self.sounds = []
        self.clock = 0

    def update(self, level, block_size):
        self.clock += 1
        if self.clock in [self.interval, self.interval-3]:
            self.sounds.append(Sound(self.loc, self.lifespan))
        if self.clock == self.interval:
            self.voice.play(maxtime=self.lifespan, fade_ms=self.lifespan//4)
            self.clock = 0
        for s in self.sounds:
            if s.update(level, block_size):
                self.sounds.remove(s)

        return None

    def draw(self, screen):
        for s in self.sounds:
            s.draw(screen)
