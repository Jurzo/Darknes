import pygame

class Level:
    def __init__(self, size):
        self.size = self.width, self.height = size
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]
        self.colors = [(0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (127, 127, 127)]

    def get_spawns(self):
        p_spawns, m_spawns = [], []
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 2:
                    cell = 0
                    p_spawns.append((x,y))
                elif cell == 3:
                    cell = 0
                    m_spawns.append((x,y))
        return p_spawns, m_spawns

    def draw(self,screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = x * 40, y * 40, 40, 40
                pygame.draw.rect(screen, self.colors[cell], rect)


def load_level(filename):
    try:
        grid = []
        with open(filename, 'r') as file:
            header = file.readline().strip('# ')
            grid_size = tuple(int(n) for n in header.split('x'))
            level = Level(grid_size)
            for line in file:
                row = []
                for char in line.strip():
                    row.append(int(char))
                grid.append(row)
            level.grid = grid
        return level
    except:
        return None

if __name__ == '__main__':
    l = load_level(input('filename: '))
    for r in l: print(r)