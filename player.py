import pygame, rock

class Player:
    def __init__(self, pos, size=20, blockSize = 40):
        self.x, self.y = pos
        self.speed = 5
        self.gridLocation = int(self.x/blockSize),int(self.y/blockSize)
        self.step = 19
        self.stepSize = 20
        self.rest = 20
        self.throwCoolDown = 100
        self.throwCoolDownCounter = 0
        self.walk_step = True
        self.moving = False
        self.size = size
        self.blockSize = blockSize
        self.channel = pygame.mixer.Channel(2)
        walk1 = pygame.mixer.Sound('src/walk_1.wav')
        walk2 = pygame.mixer.Sound('src/walk_2.wav')
        self.sounds = [walk1,walk2]

    def move(self, moveX, moveY, neighbours, level):
        self.throwCoolDownCounter -= 1
        if self.throwCoolDownCounter <= 0:
            self.throwCoolDownCounter = 0
        if self.moving:
            self.step += 1
            self.rest = 0
        else:
            self.rest += 1
        if self.step == self.stepSize:
            self.step = 0
        self.gridLocation = int(self.x/self.blockSize),int(self.y/self.blockSize)

        if level.grid[self.gridLocation[0]][self.gridLocation[1]] == 4:
            pass
        
        self.x += self.speed * moveX
        self.y += self.speed * moveY

        if self.x-self.size <= (self.gridLocation[0])*self.blockSize and neighbours[0]:
            self.x = self.gridLocation[0]*self.blockSize+self.size+1
            moveX = False
        if self.x+self.size >= (self.gridLocation[0]+1)*self.blockSize and neighbours[1]:
            self.x = (self.gridLocation[0]+1)*self.blockSize-self.size-1
            moveX = False
        if self.y-self.size <= (self.gridLocation[1])*self.blockSize and neighbours[2]:
            self.y = self.gridLocation[1]*self.blockSize+self.size+1
            moveY = False
        if self.y+self.size >= (self.gridLocation[1]+1)*self.blockSize and neighbours[3]:
            self.y = (self.gridLocation[1]+1)*self.blockSize-self.size-1
            moveY = False

        if moveX or moveY:
            self.moving = True
        else:
            self.moving = False
            if self.rest > 20:
                self.step = self.stepSize-1

    def throw_rock(self, angle):
        if self.throwCoolDownCounter == 0:
            self.throwCoolDownCounter = self.throwCoolDown
            return rock.Rock([self.x, self.y], angle)
        else:
            return None

    def play(self):
        if self.channel.get_busy():
            self.channel.stop()
        if self.walk_step:
            self.channel.play(self.sounds[0], maxtime=400)
            self.walk_step = False
        else:
            self.channel.play(self.sounds[1], maxtime=400)
            self.walk_step = True


    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), (self.x,self.y), self.size)
