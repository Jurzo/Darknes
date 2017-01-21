class Sound:
    def __init__(self, loc, lifespan, size=160):
        self.loc = loc
        self.points = []
        self.angles = []
        self.lifespan = 0
        self.maxlifespan = lifespan
        self.blockSize = size
        for i in range(0,32):
            self.points.append(self.loc)
            self.angles.append(math.pi*2/32*i)

    def update(self, grid, gridSize):
        faded = False
        for x in range(0,len(self.points)):
            stuck = False
            if self.lifespan == self.maxlifespan:
                faded = True
            else:
                self.lifespan += 1

            for j in range(0,gridSize[1]):
                for i in range(0,gridSize[0]):
                    if grid.grid[i + j*gridSize[0]] == 1:
                        if i*self.blockSize <= self.points[x][0] <= (i+1)*self.blockSize
                        and j*self.blockSize <= self.points[x][1] <= (j+1)*self.blockSize:
                            stuck = True

            if not stuck:
                self.points[x] = [self.points[x][0]+5*math.cos(self.angles[x]), self.points[x][1]+5*math.sin(self.angles[x])]

        return faded


    def draw(self, screen):
        color = 255-int(255/self.maxlifespan*self.lifespan)
        pygame.draw.aalines(screen, (color,color,color), True, self.points)
