import perlin_noise
import random



class IslandGenerator:
    def __init__(self):

        self.map = []
        self.map_width = 0
        self.map_height = 0

    def generate_island(self, width, height, frequency, octaves):
        """Generates the actual island."""

        #Uses perlin noise to generate a random noise map. Everything after
        #this line just masks the random noise to look more like an island.
        self.map = perlin_noise.PerlinNoiseGenerator().generate_noise(width,
                                                                      height,
                                                                      frequency,
                                                                      octaves)
        self.map_width = width
        self.map_height = height
        

        return self.map
