import pygame, math

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
        
class Sound:
    def __init__(self, loc, lifespan):
        self.loc = loc
        self.points = []
        self.angles = []
        self.lifespan = 0
        self.maxlifespan = lifespan
        for i in range(0,32):
            self.points.append(self.loc)
            self.angles.append(math.pi*2/32*i)

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
##        for p in self.points:
##            pygame.draw.circle(screen,(255,255,255),(int(p[0][0]),int(p[0][1])),2,2)
##    

def draw(screen, objects = None):
    if objects:
        for o in objects:
            o.draw(screen)

def setup():
    width = 1280
    height = 720
    screen = pygame.display.set_mode((width,height))
    return screen

def main():
    clock = pygame.time.Clock()
    screen = setup()
    field = pygame.Surface((2560,1440))
    objects = []
    walls = []
    camOffSet = [0,0]
    camMovement = [0,0]
    walls.append(Map([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,
                        0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,
                        0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,
                        0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,
                        0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,
                        0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,
                        0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,]))
    
    while True:
        clock.tick(30)
        screen.fill((0,0,0))
        field.fill((0,0,0))
        draw(field,walls)
        draw(field,objects)
        camOffSet[0],camOffSet[1] = camOffSet[0]+camMovement[0],camOffSet[1]+camMovement[1]
        screen.blit(field,camOffSet)
        pygame.display.flip()
        for o in objects:
            if o.update(walls[0]):
                objects.remove(o)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                xpos, ypos = pygame.mouse.get_pos()
                xpos, ypos = xpos-camOffSet[0], ypos-camOffSet[1]
                objects.append(Sound([xpos,ypos],1000))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    camMovement[1] = -10
                elif event.key == pygame.K_DOWN:
                    camMovement[1] = 10
                elif event.key == pygame.K_LEFT:
                    camMovement[0] = -10
                elif event.key == pygame.K_RIGHT:
                    camMovement[0] = 10
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if camMovement[1] == -10:
                        camMovement[1] = 0
                elif event.key == pygame.K_DOWN:
                    if camMovement[1] == 10:
                        camMovement[1] = 0
                elif event.key == pygame.K_LEFT:
                    if camMovement[0] == -10:
                        camMovement[0] = 0
                elif event.key == pygame.K_RIGHT:
                    if camMovement[0] == 10:
                        camMovement[0] = 0
                
main()
