import pygame



class Map:


    def __init__(self, type, map):

        self.type = type
        self.map = map
        self.width = len(self.map[0])
        self.height = len(self.map)
        self.cell_size = 4

        self.waterline = 0
        
        self.minimap = pygame.Surface((self.width * self.cell_size,
                                       self.height * self.cell_size))
        self.draw_minimap()


    def get_waterline(self):
        waterline_divide = 0.05 # normally, it was .60

        values = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                values.append(self.map[y][x])
        values.sort()

        return values[int((len(values)-1)*waterline_divide)]
        

    def draw_minimap(self):

        self.waterline = self.get_waterline()
        print(self.waterline)

        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.map[y][x] > 255.0:
                    self.map[y][x] = 255.0
                cell = int(self.map[y][x])

                if cell <= self.waterline:
                    color = (25, 25, cell+75) # eau
                elif cell > self.waterline and cell <= self.waterline + 10:
                    color = (cell+80, cell+80, 100) # plage
                elif cell > self.waterline + 10:
                    color = (0, 255-cell, 0) # terrain

                #color = (cell, cell, cell)
                
                image = pygame.Surface((self.cell_size, self.cell_size))
                image.fill(color)
                self.minimap.blit(image, (x * self.cell_size,
                                          y * self.cell_size))
