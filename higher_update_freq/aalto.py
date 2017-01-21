import pygame, math
from player import Player

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
        for i in range(0,64):
            self.points.append(self.loc)
            self.angles.append(math.pi*2/64*i)

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
                self.points[x] = [self.points[x][0]+10*math.cos(self.angles[x]), self.points[x][1]+10*math.sin(self.angles[x])]

        return dead


    def draw(self, screen):
        color = 255-int(255/self.maxlifespan*self.lifespan)
        pygame.draw.aalines(screen, (color,color,color), True, self.points)    

def draw(screen, objects = None):
    if objects:
        for o in objects:
            o.draw(screen)

def checkMove(playerLoc, grid):
    neighbours = [False,False,False,False]
    gridLocation = (int(playerLoc[0]/80),int(playerLoc[1]/80))
    if gridLocation[0] > 0:
        if grid[gridLocation[0]-1 +gridLocation[1]*16] == 1:
            neighbours[0] = True
    if gridLocation[0] < 16:
        if grid[gridLocation[0]+1 +gridLocation[1]*16] == 1:
            neighbours[1] = True
    if gridLocation[1] > 0:
        if grid[gridLocation[0]+(gridLocation[1]-1)*16] == 1:
            neighbours[2] = True
    if gridLocation[0] < 16:
        if grid[gridLocation[0]+(gridLocation[1]+1)*16] == 1:
            neighbours[3] = True

    return neighbours
            

def setup():
    width = 1280
    height = 720
    screen = pygame.display.set_mode((width,height))
    return screen

def main():
    clock = pygame.time.Clock()
    screen = setup()
    field = pygame.Surface((2560,1440))
    player = Player((350,420))
    objects = []
    walls = []
    camOffSet = [0,0]
    camMovement = [0,0]
    walls.append(Map([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
                      1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
                      1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,
                      1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,
                      1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,
                      1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,
                      1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,
                      1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,
                      1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]))

    moveU, moveD, moveL, moveR = False, False, False, False
    
    while True:
        clock.tick(30)
        screen.fill((0,0,0))
        field.fill((0,0,0))
##        draw(field,walls)
        draw(field,objects)
        player.draw(field)
        camOffSet[0],camOffSet[1] = 1280/2-player.x, 720/2-player.y
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
                    moveU = True
                elif event.key == pygame.K_DOWN:
                    moveD = True
                elif event.key == pygame.K_LEFT:
                    moveL = True
                elif event.key == pygame.K_RIGHT:
                    moveR = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    moveU = False
                elif event.key == pygame.K_DOWN:
                    moveD = False
                elif event.key == pygame.K_LEFT:
                    moveL = False
                elif event.key == pygame.K_RIGHT:
                    moveR = False
        neighbours = checkMove((player.x,player.y), walls[0].grid)
        if player.step == 0:
            objects.append(Sound([player.x+(moveR-moveL)*15,player.y+(moveD-moveU)*15],2000))
        player.move(moveR-moveL, moveD-moveU, neighbours)
                
main()
