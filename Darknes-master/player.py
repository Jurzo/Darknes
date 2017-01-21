import pygame

class Player:
    def __init__(self, pos, size=30, blockSize = 40):
        self.x, self.y = pos
        self.speed = 5
        self.gridLocation = int(self.x/blockSize),int(self.y/blockSize)
        self.step = 19
        self.stepSize = 20
        self.rest = 20
        self.moving = False
        self.size = size
        self.blockSize = blockSize

    def move(self, moveX, moveY, neighbours):
        if self.moving:
            self.step += 1
            self.rest = 0
        else:
            self.rest += 1
        if self.step == self.stepSize:
            self.step = 0
        self.gridLocation = int(self.x/self.blockSize),int(self.y/self.blockSize)
        
        self.x += self.speed * moveX
        self.y += self.speed * moveY

        if self.x-self.size <= (self.gridLocation[0])*self.blockSize and neighbours[0]:
            self.x = self.gridLocation[0]*self.blockSize+self.size+1
            moveX = False
        elif self.x+self.size >= (self.gridLocation[0]+1)*self.blockSize and neighbours[1]:
            self.x = (self.gridLocation[0]+1)*self.blockSize-self.size-1
            moveX = False
        if self.y-self.size <= (self.gridLocation[1])*self.blockSize and neighbours[2]:
            self.y = self.gridLocation[1]*self.blockSize+self.size+1
            moveX = False
        elif self.y+self.size >= (self.gridLocation[1]+1)*self.blockSize and neighbours[3]:
            self.y = (self.gridLocation[1]+1)*self.blockSize-self.size-1
            moveX = False

        if moveX or moveY:
            self.moving = True
        else:
            self.moving = False
            if self.rest > 20:
                self.step = self.stepSize-1


    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), (self.x,self.y), self.size)
