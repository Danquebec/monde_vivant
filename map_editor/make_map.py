#!/usr/bin/python
# -*- coding:utf-8 -*-

# Monde vivant’s map editor © 2013 Daniel Dumaresq
# e-mail: danquebec@singularity.fr
# Jabber: danquebec@linkmauve.org

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License v3
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pickle

class Map():
    '''Manages the map.'''
    def __init__(self):
        self.array = []
        self.number_of_layers = 0
        self.file_read = None

    def new(self, cells):
        '''Creates the array of the map and sets the number of layers.'''
        def get_columns(cells_y):
            column = [[0, 0, 0] for cell in range(0, cells_y)]
            return column
        self.array = [get_columns(cells[1]) for column in range(0, cells[0])]
        self.number_of_layers = len(self.array[0][0])

    def draw(self, cell, present_layer, image_selected):
        '''Manages the “drawing” applied on the array. With an image selected
        in the list of images and a layer selected in the menu, the users 
        presses the mouse on array grid, where it adds the image selected on 
        the layer selected in the array.'''
        self.array[cell[0]][cell[1]][present_layer] = image_selected

    def save(self):
        '''Saves the array to a file called “map”.'''
        with open('map', 'wb') as file_write:
            pickle.dump(self.array, file_write)
            print('Map saved!')
