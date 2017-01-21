import pygame
import random

pygame.init()

width = 800
height = 600

FPS = 15

block_size = 10

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')

font = pygame.font.SysFont(None, 25)

def Snake(snakelist, block_size):
    for XnY in snakelist:
        pygame.draw.rect(gameDisplay, black, [XnY[0], XnY[1], block_size, block_size])

def message_to_screen(msg, color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [width/2, height/2])

clock = pygame.time.Clock()

def gameLoop():
    gameExit = False
    gameOver = False

    first_x = width/2
    first_y = height/2
    first_x_change = 0
    first_y_change = 0

    snakelist = []
    snakeLength = 1

    randAppleX = round(random.randrange(0, width-block_size)/10.0)*10.0
    randAppleY = round(random.randrange(0, height-block_size)/10.0)*10.0

    while not gameExit:

        while gameOver:
            gameDisplay.fill(white)
            message_to_screen("Game over, press A to play again or Q to quit", red)
            pygame.display.update()
            snakelist = []
            snakeLength = 1

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        gameLoop()

                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and first_x_change == 0:
                    first_y_change = 0
                    first_x_change = -block_size
                if event.key == pygame.K_RIGHT and first_x_change == 0:
                    first_y_change = 0
                    first_x_change = block_size
                if event.key == pygame.K_UP and first_y_change == 0:
                    first_x_change = 0
                    first_y_change = -block_size
                if event.key == pygame.K_DOWN and first_y_change == 0:
                    first_x_change = 0
                    first_y_change = block_size

        if first_x < 0 or first_x >= width or first_y < 0 or first_y >= height:
            gameOver = True

        first_x += first_x_change
        first_y += first_y_change

        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, block_size, block_size])

        snakeHead = []
        snakeHead.append(first_x)
        snakeHead.append(first_y)
        snakelist.append(snakeHead)

        if len(snakelist) > snakeLength:
            del snakelist[0]

        for eachSegment in snakelist[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        Snake(snakelist, block_size)
        pygame.display.update()

        #if first_x == randAppleX and first_y == randAppleY:
         #   randAppleX = round(random.randrange(0, width-block_size)/10.0)*10.0
          #  randAppleY = round(random.randrange(0, height-block_size)/10.0)*10.0
           # snakeLength += 1

        if first_x >= randAppleX and first_x <= randAppleX+block_size:
            if first_y >= randAppleY and first_y <= randAppleY+block_size:
                randAppleX = round(random.randrange(0, width-block_size)/10.0)*10.0
                randAppleY = round(random.randrange(0, height-block_size)/10.0)*10.0
                snakeLength += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

gameLoop()
