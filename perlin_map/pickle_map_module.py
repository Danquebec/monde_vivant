# coding: utf-8
import pickle

class PickleMap():
    def __init__(self):
        self.pickle_map = []
        self.blocking_cells = []
        self.height = 0
        self.width = 0

    def find_terrain(self, width, height, waterline, map_):
        for y in range(0, height):
            row = []
            for x in range(0, width):
                if map_[y][x] > 255.0:
                    map_[y][x] = 255.0
                cell = int(map_[y][x])

                if cell <= waterline:
                    row.append(['water', 0, 0]) # eau
                elif cell > waterline and cell <= waterline + 50:
                    row.append(['sand', 0, 0]) # plage
                elif cell > waterline + 50:
                    row.append(['grass', 0, 0]) # terrain
            self.pickle_map.append(row)
        self.height = len(self.pickle_map)
        self.width = len(self.pickle_map[0])

    def find_blocking_cells(self):
        for row in self.pickle_map:
            b_row = []
            for cell in row:
                if cell[0] == 'water':
                    b_row.append(1)
                else:
                    b_row.append(0)
            self.blocking_cells.append(b_row)

    def double_size(self):
        new_map = []
        new_blocking_cells = []
        
        for y in range(0, self.height):
            row = []
            b_row = []
            for x in range(0, self.width):
                row.append(self.pickle_map[y][x])
                row.append(self.pickle_map[y][x])
                b_row.append(self.blocking_cells[y][x])
                b_row.append(self.blocking_cells[y][x])
            new_map.append(row)
            new_map.append(row)
            new_blocking_cells.append(b_row)
            new_blocking_cells.append(b_row)

        self.pickle_map = new_map
        self.blocking_cells = new_blocking_cells

    def dump_map(self):
        print(len(self.pickle_map), len(self.pickle_map[0]))
        with open('map', 'wb') as f:
            pickle.dump({'map':self.pickle_map,
                         'blocking_cells':self.blocking_cells}, f)
