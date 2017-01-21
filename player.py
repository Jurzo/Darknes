import pygame

class Player:
    def __init__(self, pos):
        self.x, self.y = pos
        self.speed = 5
        self.gridLocation = int(self.x/80),int(self.y/80)
        self.step = 0
        self.stepSize = 10

    def move(self, moveX, moveY, neighbours):
        self.step += 1
        if self.step == self.stepSize:
            self.step = 0
        self.gridLocation = int(self.x/80),int(self.y/80)     
        
        self.x += self.speed * moveX
        self.y += self.speed * moveY

        if self.x-20 <= (self.gridLocation[0])*80 and neighbours[0]:
            self.x = self.gridLocation[0]*80+20
        if self.x+20 >= (self.gridLocation[0]+1)*80 and neighbours[1]:
            self.x = (self.gridLocation[0]+1)*80-20
        if self.y-20 <= (self.gridLocation[1])*80 and neighbours[2]:
            self.y = self.gridLocation[1]*80+20
        if self.y+20 >= (self.gridLocation[1]+1)*80 and neighbours[3]:
            self.y = (self.gridLocation[1]+1)*80-20


    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), (self.x,self.y), 20)
