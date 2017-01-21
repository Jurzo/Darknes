import pygame, math

class Rock:
    def __init__(self, loc, dir):
        self.loc = loc
        self.lastLoc = loc
        self.dir = dir
        self.travel = 0
        self.maxtravel = 40
        self.stuck = False
        self.channel = pygame.mixer.Channel(3)
        self.voice = pygame.mixer.Sound('src/rock.wav')

    def update(self, level, block_size):
        self.travel += 1
        x, y = (int(self.loc[0] / block_size), int(self.loc[1] / block_size))

        if level.grid[y][x] == 1 or self.travel == self.maxtravel:
            self.stuck = True

        if not self.stuck:
            self.lastLoc = self.loc
            self.loc = [self.loc[0] + 10 * math.cos(self.dir), self.loc[1] + 10 * math.sin(self.dir)]

        if self.stuck:
            self.voice.play()
            return self.lastLoc
        else:
            return None

    def draw(self, surface):
        pygame.draw.circle(surface, (255,0,0),(int(self.loc[0]),int(self.loc[1])), 10)