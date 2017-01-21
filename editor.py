import pygame
import loader

class EditorInstance:
    def __init__(self):
        self.pen_size = 1
        self.xlock, self.ylock = -1, -1

        self.block_size = 8
        self.level = loader.Level((80, 80))
        
        self.brush = 1
        self.hotkeys = {pygame.K_0: 0, pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6}
        self.block_types = ['air', 'wall', 'player spawn', 'monster spawn', 'finish', 'half wall', 'sound Source']
        self.colors = [(0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (127,127,127), (0,255,255)]

        self.size = self.block_size * self.level.width, self.block_size * self.level.height

        self.display = pygame.display.set_mode(self.size)
        pygame.display.set_caption('level %dx%d | brush %d: %s | pen size: %d'
                                   % (self.level.width, self.level.height, self.brush,
                                      self.block_types[self.brush], self.pen_size))
        self.display.fill(self.colors[0])

        self.running = True



        

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.block_size -= 1
                    self.render_all()
                if event.key == pygame.K_w:
                    self.block_size += 1
                    self.render_all()
                if event.key == pygame.K_d:
                    self.change_size()
                if event.key == pygame.K_z:
                    self.xlock = pygame.mouse.get_pos()[0] // self.block_size if self.xlock < 0 else -1
                if event.key == pygame.K_x:
                    self.ylock = pygame.mouse.get_pos()[1] // self.block_size if self.ylock < 0 else -1
                if event.key == pygame.K_s:
                    self.save_level()
                if event.key == pygame.K_l:
                    loaded = loader.load_level(input('file to load: '))
                    if loaded:
                        self.level = loaded
                        self.render_all()
                    else:
                        print('Loading error!')
                if event.key in self.hotkeys:
                    self.brush = self.hotkeys[event.key]
            elif event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.pen_size += 1
                elif event.button == 5 and self.pen_size > 1:
                    self.pen_size -= 1
        if pygame.mouse.get_pressed()[0] == True:
            xpos, ypos = pygame.mouse.get_pos()
            xpos = xpos // self.block_size if self.xlock < 0 else self.xlock
            ypos = ypos // self.block_size if self.ylock < 0 else self.ylock
            for y in range(ypos, ypos + self.pen_size):
                if y >= self.level.height: continue
                for x in range(xpos, xpos + self.pen_size):
                    if x >= self.level.width: continue
                    if self.level.grid[y][x] != self.brush:
                        self.level.grid[y][x] = self.brush
                        pygame.draw.rect(self.display, self.colors[self.brush],
                                         [x * self.block_size, y * self.block_size,
                                          self.block_size, self.block_size])
        elif pygame.mouse.get_pressed()[2] == True:
            xpos, ypos = pygame.mouse.get_pos()
            xpos = xpos // self.block_size if self.xlock < 0 else self.xlock
            ypos = ypos // self.block_size if self.ylock < 0 else self.ylock
            for y in range(ypos, ypos + self.pen_size):
                if y >= self.level.height: continue
                for x in range(xpos, xpos + self.pen_size):
                    if x >= self.level.width: continue
                    if self.level.grid[y][x] != 0:
                        self.level.grid[y][x] = 0
                        pygame.draw.rect(self.display, self.colors[0],
                                         [x * self.block_size, y * self.block_size,
                                          self.block_size, self.block_size])
        pygame.display.set_caption('level %dx%d | brush %d: %s | pen size: %d | %s'
                                   % (self.level.width, self.level.height, self.brush,
                                      self.block_types[self.brush], self.pen_size,
                                      '' + 'x' * (self.xlock >= 0) + 'y' * (self.ylock >= 0)))
        pygame.display.flip()
        return True

    def change_size(self):
        width, height = int(input('width: ')), int(input('height: '))
        if width > 1 and height > 1:
            new_level = loader.Level((width, height))
            min_width = min(width, self.level.width)
            min_height = min(height, self.level.height)
            for y in range(min_height):
                for x in range(min_width):
                    new_level.grid[y][x] = self.level.grid[y][x]
            self.level = new_level
            self.level.size
            self.render_all()



    def render_all(self):
        self.size = self.block_size * self.level.width, self.block_size * self.level.height
        self.display = pygame.display.set_mode(self.size)
        for y, row in enumerate(self.level.grid):
            for x, cell in enumerate(row):
                pygame.draw.rect(self.display, self.colors[cell],
                                 [x * self.block_size, y * self.block_size,
                                  self.block_size, self.block_size])

    def save_level(self):
        filename = input('file to save: ')
        if filename:
            with open(filename, 'w') as file:
                file.write('# %dx%d\n' % self.level.size)
                file.write('\n'.join(''.join(str(square) for square in row) for row in self.level.grid))


def main():
    pygame.init()
    editor = EditorInstance()
    while editor.loop(): pass


if __name__ == '__main__':
    main()
