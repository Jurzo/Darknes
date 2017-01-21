import pygame

class Player:
    def __init__(self, pos):
        self.x, self.y = pos
        self.speed = 2
        self.gridLocation = int(self.x/80),int(self.y/80)
        self.step = 39
        self.stepSize = 40
        self.rest = 40
        self.moving = False

    def move(self, moveX, moveY, neighbours):
        if self.moving:
            self.step += 1
            self.rest = 0
        else:
            self.rest += 1
        if self.step == self.stepSize:
            self.step = 0
        self.gridLocation = int(self.x/80),int(self.y/80)
        
        self.x += self.speed * moveX
        self.y += self.speed * moveY

        if self.x-20 <= (self.gridLocation[0])*80 and neighbours[0]:
            self.x = self.gridLocation[0]*80+20
            moveX = False
        if self.x+20 >= (self.gridLocation[0]+1)*80 and neighbours[1]:
            self.x = (self.gridLocation[0]+1)*80-20
            moveX = False
        if self.y-20 <= (self.gridLocation[1])*80 and neighbours[2]:
            self.y = self.gridLocation[1]*80+20
            moveX = False
        if self.y+20 >= (self.gridLocation[1]+1)*80 and neighbours[3]:
            self.y = (self.gridLocation[1]+1)*80-20
            moveX = False

        if moveX or moveY:
            self.moving = True
        else:
            self.moving = False
            if self.rest > 40:
                self.step = self.stepSize-1


    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), (self.x,self.y), 20)
