class Level:
    def __init__(self, size):
        self.size = self.width, self.height = size
        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]


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