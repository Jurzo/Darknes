class Map:
    def __init__(self,grid):
        self.width = 16
        self.height = 9
        self.size = 80
        self.grid = grid

    def draw(self,screen):
        for j in range(self.height):
            for i in range(self.width):
                if self.grid[i +j*self.width] == 1:
                    rect = self.size*i, self.size*j, self.size, self.size
                    pygame.draw.rect(screen, (255,255,255), rect)
