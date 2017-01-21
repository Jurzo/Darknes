import math, pygame

class Sound:
    def __init__(self, loc, lifespan):
        self.loc = loc
        self.points = []
        self.angles = []
        self.lifespan = 0
        self.maxlifespan = lifespan
        for i in range(0,128):
            self.points.append(self.loc)
            self.angles.append(math.pi*2/128*i)

    def update(self, grid):
        dead = False
        for x in range(0,len(self.points)):
            stuck = False
            if self.lifespan == self.maxlifespan:
                dead = True
            else:
                self.lifespan += 1

            for j in range(0,9):
                for i in range(0,16):
                    if grid.grid[i + j*16] == 1:
                        if i*80 <= self.points[x][0] <= (i+1)*80 and j*80 <= self.points[x][1] <= (j+1)*80:
                            stuck = True

            if not stuck:
                self.points[x] = [self.points[x][0]+5*math.cos(self.angles[x]), self.points[x][1]+5*math.sin(self.angles[x])]

        return dead


    def draw(self, screen):
        color = 255-int(255/self.maxlifespan*self.lifespan)
        pygame.draw.aalines(screen, (color,color,color), True, self.points)
