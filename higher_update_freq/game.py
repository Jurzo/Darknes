import pygame, math
from player import Player
from sound import Sound

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
    drawing = True
    
    while True:
        clock.tick(60)
        screen.fill((0,0,0))
        field.fill((0,0,0))
##        draw(field,walls)
        if drawing:
            draw(field,objects)
            player.draw(field)
            camOffSet[0],camOffSet[1] = 1280/2-player.x, 720/2-player.y
            screen.blit(field,camOffSet)
            pygame.display.flip()
            drawing = False
        else:
            drawing = True
        for o in objects:
            if o.update(walls[0]):
                objects.remove(o)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0
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
        if player.step == 0 or player.step == 8:
            player.step += 1
            objects.append(Sound([player.x+(moveR-moveL)*15,player.y+(moveD-moveU)*15],4000))
        player.move(moveR-moveL, moveD-moveU, neighbours)
                
main()
