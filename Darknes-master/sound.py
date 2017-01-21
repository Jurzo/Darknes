import math, pygame

class Sound:
    def __init__(self, loc, lifespan=2000, high=False):
        self.loc = loc
        self.points = []
        self.angles = []
        self.lifespan = 0
        self.maxlifespan = lifespan
        self.high = high
        for i in range(0,64):
            self.points.append(self.loc)
            self.angles.append(math.pi*2/64*i)

    def update(self, level, block_size):
        dead = False
        for i, point in enumerate(self.points):
            stuck = False
            if self.lifespan == self.maxlifespan:
                dead = True
            else:
                self.lifespan += 1
            x, y = (int(point[0] / block_size), int(point[1] / block_size))
            if level.grid[y][x] == 1:
                stuck = True
            elif level.grid[y][x] == 5 and not self.high:
                stuck = True

            # for j in range(level.height):
            #     for i in range(level.width):
            #         if level.grid[i][j] in [1, 5]:
            #             if i*block_size <= self.points[x][0] <= (i+1)*block_size and j*block_size <= self.points[x][1] <= (j+1)*block_size:
            #                 stuck = True

            if not stuck:
                self.points[i] = [point[0]+10*math.cos(self.angles[i]), point[1]+10*math.sin(self.angles[i])]

        return dead


    def draw(self, screen):
        color = 255-int(255/self.maxlifespan*self.lifespan)
        pygame.draw.aalines(screen, (color,color,color), True, self.points)
