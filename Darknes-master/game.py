import pygame, math, loader, random
from player import Player
from sound import Sound

class Game:
    def draw(self, screen, objects = None):
        if objects:
            for o in self.objects:
                o.draw(screen)

    def checkMove(self):
        neighbours = [False,False,False,False]
        x, y = (self.player.x // self.block_size, self.player.y // self.block_size)
        walls = [1, 5]
        if x > 0:
            if self.level.grid[y][x-1] in walls:
                neighbours[0] = True
        if x < self.level.width:
            if self.level.grid[y][x+1] in walls:
                neighbours[1] = True
        if y > 0:
            if self.level.grid[y-1][x] in walls:
                neighbours[2] = True
        if y < self.level.height:
            if self.level.grid[y+1][x] in walls:
                neighbours[3] = True

        return neighbours


    def setup(self):
        width = 1280
        height = 720
        screen = pygame.display.set_mode((width,height))
        return screen

    def __init__(self):
        self.block_size = 40
        self.level = loader.load_level('1.level')
        self.clock = pygame.time.Clock()
        self.screen = self.setup()
        self.field = pygame.Surface((self.level.width * self.block_size, self.level.height * self.block_size))
        p_spawns, m_spawns = self.level.get_spawns()
        p_spawn, m_spawn = random.choice(p_spawns), random.choice(m_spawns)
        self.player = Player(tuple(self.block_size * i + 40 for i in p_spawn))
        self.objects = []
        self.camOffSet = [0,0]
        self.camMovement = [0,0]

        # level =      Map([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        #                   1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,
        #                   1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,
        #                   1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,
        #                   1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,
        #                   1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,
        #                   1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,
        #                   1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,
        #                   1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])

        self.moveU, self.moveD, self.moveL, self.moveR = False, False, False, False

        while True:
            self.clock.tick(30)
            self.screen.fill((0,0,0))
            self.field.fill((0,0,0))
    ##        draw(field,level)
    ##        self.level.draw(self.field)
            self.draw(self.field,self.objects)
            self.player.draw(self.field)
            self.camOffSet = [1280/2-self.player.x, 720/2-self.player.y]
            self.screen.blit(self.field,self.camOffSet)
            pygame.display.flip()
            for o in self.objects:
                if o.update(self.level, self.block_size):
                    self.objects.remove(o)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == pygame.MOUSEBUTTONUP:
                    xpos, ypos = pygame.mouse.get_pos()
                    xpos, ypos = xpos-self.camOffSet[0], ypos-self.camOffSet[1]
                    self.objects.append(Sound([xpos,ypos],1000))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.moveU = True
                    elif event.key == pygame.K_DOWN:
                        self.moveD = True
                    elif event.key == pygame.K_LEFT:
                        self.moveL = True
                    elif event.key == pygame.K_RIGHT:
                        self.moveR = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.moveU = False
                    elif event.key == pygame.K_DOWN:
                        self.moveD = False
                    elif event.key == pygame.K_LEFT:
                        self.moveL = False
                    elif event.key == pygame.K_RIGHT:
                        self.moveR = False
            neighbours = self.checkMove()
            if self.player.step == 0 or self.player.step == 4:
                self.player.step += 1
                self.objects.append(Sound([self.player.x+(self.moveR-self.moveL)*15,
                                           self.player.y+(self.moveD-self.moveU)*15],2000))
                self.objects.append(Sound([self.player.x + (self.moveR - self.moveL) * 15,
                                           self.player.y + (self.moveD - self.moveU) * 15], 2000, True))
            self.player.move(self.moveR-self.moveL, self.moveD-self.moveU, neighbours)
                
def main():
    game = Game()

if __name__ == '__main__':
    main()