import math, pygame

class Sound:
    def __init__(self, loc, lifespan=2000, stop_at = [1,5], res = 64, color = (255,255,255)):
        self.loc = loc
        self.points = []
        self.angles = []
        self.lifespan = 0
        self.maxlifespan = lifespan
        self.stop_at = stop_at
        self.res = res
        self.color = color
        for i in range(0,res):
            self.points.append(self.loc)
            self.angles.append(math.pi*2/res*i)

    def update(self, level, block_size):
        dead = False
        for i, point in enumerate(self.points):
            stuck = False
            if self.lifespan == self.maxlifespan:
                dead = True
            else:
                self.lifespan += 1
            x, y = (int(point[0] / block_size), int(point[1] / block_size))
            if level.grid[y][x] in self.stop_at:
                stuck = True

            if not stuck:
                self.points[i] = [point[0]+10*math.cos(self.angles[i]), point[1]+10*math.sin(self.angles[i])]

        return dead


    def draw(self, screen):
        color = tuple(c-int(c/self.maxlifespan*self.lifespan) for c in self.color)
        pygame.draw.aalines(screen, color, True, self.points)