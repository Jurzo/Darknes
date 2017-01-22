import pygame, math, loader, random
from player import Player
from sound import Sound
from soundSource import Source

class Game:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.set_num_channels(20)
        self.background = pygame.mixer.Channel(1)
        self.background_sound = pygame.mixer.Sound('src/ambient.wav')
        pygame.mixer.set_reserved(3)
        pygame.init()
        self.clock = pygame.time.Clock()
        info = pygame.display.Info()
        self.width, self.height = info.current_w, info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.field = None
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.font = pygame.font.SysFont('Consolas', 30)

    def load_level(self, filepath):
        self.level_won, self.level_lost = False, False
        self.block_size = 40
        self.level = loader.load_level(filepath)
        if self.field: del self.field
        self.field = pygame.Surface((self.level.width * self.block_size, self.level.height * self.block_size))
        self.countdown = self.level.time_limit
        p_spawns, m_spawns = self.level.get_spawns()
        p_spawn, m_spawn = random.choice(p_spawns), random.choice(m_spawns)
        self.player = Player(tuple(self.block_size * i + 40 for i in p_spawn))
        self.objects = []
        self.soundObjects = []
        for y, row in enumerate(self.level.grid):
            for x, cell in enumerate(row):
                if cell == 6:
                    source = Source([x*self.block_size+self.block_size/2,y*self.block_size+self.block_size/2],
                                    'src/drop-1.wav',random.randint(100,250), random.randint(1500,2500), color=(0,0,255))
                    source.clock = random.randint(0,source.interval-1)
                    self.soundObjects.append(source)
                elif cell == 7:
                    source = Source([x*self.block_size+self.block_size/2,y*self.block_size+self.block_size/2],
                                    'src/drop-1.wav',random.randint(75,100), random.randint(5000,6000),color=(0,255,255))
                    source.clock = random.randint(0,source.interval-1)
                    self.soundObjects.append(source)
                elif cell == 4:
                    source = Source(
                        [x * self.block_size + self.block_size / 2, y * self.block_size + self.block_size / 2],
                        None, 100, 400, color=(0,255,0))
                    source.clock = random.randint(0, source.interval - 1)
                    self.soundObjects.append(source)
        self.camOffSet = [0,0]
        self.moveU, self.moveD, self.moveL, self.moveR = False, False, False, False

    def draw(self, screen, objects = None):
        if objects:
            for o in objects:
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



    def loop(self):
        self.clock.tick(30)
        self.screen.fill((0,0,0))
        self.field.fill((0,0,0))
##        draw(field,level)
##        self.level.draw(self.field)
##        for block in self.goal:
##            pygame.draw.rect(self.field, (58, 178, 7), block)
        self.draw(self.field, self.soundObjects)
        self.draw(self.field, self.objects)
##        for s in self.soundObjects:
##            s.draw(self.field)
        self.player.draw(self.field)
        self.camOffSet = [self.width/2-self.player.x, self.height/2-self.player.y]
        self.screen.blit(self.field,self.camOffSet)
        if self.countdown >= 0:
            print(self.countdown)
            self.screen.blit(self.font.render('%d:%.2d' % divmod(self.countdown, 60), True, (255,255,255)), (self.width - 100, 0))
        pygame.display.flip()
        if not self.background.get_busy():
            self.background.play(self.background_sound)
        for o in self.objects:
            stopped = o.update(self.level, self.block_size)
            if stopped:
                self.objects.remove(o)
                if not stopped == True:
                    self.objects.append(Sound(stopped))
                    self.objects.append(Sound(stopped, stop_at = [1]))
        for s in self.soundObjects:
            if s.voice != None:
                dist_to_source = math.sqrt((self.player.x-s.loc[0])**2 + (self.player.y-s.loc[1])**2)
                vol = 1 / (1 + math.exp(-(100 / dist_to_source))) - 0.43
                if vol < 0.1: vol = 0
                s.voice.set_volume(vol)
            s.update(self.level, self.block_size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                xpos, ypos = pygame.mouse.get_pos()
                xpos, ypos = xpos-self.camOffSet[0], ypos-self.camOffSet[1]
                angle = math.atan2(ypos - self.player.y, xpos - self.player.x)
                if (angle < 0):
                    angle += 2*math.pi
                rock = self.player.throw_rock(angle)
                if rock:
                    self.objects.append(rock)
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP,pygame.K_w]:
                    self.moveU = True
                elif event.key in [pygame.K_DOWN,pygame.K_s]:
                    self.moveD = True
                elif event.key in [pygame.K_LEFT,pygame.K_a]:
                    self.moveL = True
                elif event.key in [pygame.K_RIGHT,pygame.K_d]:
                    self.moveR = True
                elif event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    return False
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP,pygame.K_w]:
                    self.moveU = False
                elif event.key in [pygame.K_DOWN,pygame.K_s]:
                    self.moveD = False
                elif event.key in [pygame.K_LEFT,pygame.K_a]:
                    self.moveL = False
                elif event.key in [pygame.K_RIGHT,pygame.K_d]:
                    self.moveR = False
            elif event.type == pygame.USEREVENT and not (self.level_won or self.level_lost) and self.countdown >= 0:
                self.countdown -= 1
                if self.countdown == 0: self.level_lost = True

        neighbours = self.checkMove()
        if self.player.step == 0 or self.player.step == 4:
            if self.player.step == 0:
                self.player.play()
            self.player.step += 1
            self.objects.append(Sound([self.player.x+(self.moveR-self.moveL)*15,
                                       self.player.y+(self.moveD-self.moveU)*15],2000))
            self.objects.append(Sound([self.player.x + (self.moveR - self.moveL) * 15,
                                       self.player.y + (self.moveD - self.moveU) * 15], 2000, [1]))
        self.player.move(self.moveR-self.moveL, self.moveD-self.moveU, neighbours, self.level)
        if self.level.grid[self.player.gridLocation[1]][self.player.gridLocation[0]] == 4:
            self.level_won = True
        return True
                
def main(levels, loss_screen):
    game = Game()
    current_level = 0
    game.load_level(levels[current_level])
    while game.loop():
        if game.level_won:
            current_level = (current_level + 1) % len(levels)
            game.load_level(levels[current_level])
        elif game.level_lost:
            game.load_level(loss_screen)


if __name__ == '__main__':
    main(['src/opening.level', 'src/1.level', 'src/2.level', 'src/3.level', 'src/credits.level'],'src/loss.level')