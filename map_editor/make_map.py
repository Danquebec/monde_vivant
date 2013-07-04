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
        self.map = []
        self.blocking_cells = []
        self.number_of_layers = 0
        self.file_read = None

    def new(self, cells):
        '''Creates the array of the map and sets the number of layers.'''
        self.map = [[[0 for _ in xrange(3)] for _ in xrange(cells[1])] for _ in range(cells[0])]
        '''
        def get_columns(what, cells_y):
            column = [what for cell in range(0, cells_y)]
            return column
        self.map = [get_columns([0, 0, 0], cells[1]) for column in range(0, cells[0])]
        '''
        self.number_of_layers = len(self.map[0][0])
        self.blocking_cells = [[0 for _ in xrange(cells[1])] for _ in range(cells[0])]
        print(cells[0])
        for column in self.map:
            print(column)

    def add_cells(self, cell, present_layer, image_selected):
        '''Manages the “drawing” applied on the array. With an image selected
        in the list of images and a layer selected in the menu, the users 
        presses the mouse on array grid, where it adds the image selected on 
        the layer selected in the array.'''
        try:
            self.map[cell[0]][cell[1]][present_layer] = image_selected
        except IndexError:
            for column in self.map:
                print(column)
            print('cell[0]:{}'.format(cell[0]))
            print('cell[1]:{}'.format(cell[1]))
            print(present_layer)

    def add_blocking_cells(self, cell):
        if self.blocking_cells[cell[0]][cell[1]] == 0:
            self.blocking_cells[cell[0]][cell[1]] = 1
        elif self.blocking_cells[cell[0]][cell[1]] == 1:
            self.blocking_cells[cell[0]][cell[1]] = 0
        print(self.blocking_cells)

    def save(self):
        '''Saves the array to a file called “map”.'''
        with open('map', 'wb') as file_write:
            
            pickle.dump({'map':self.map,'blocking_cells':self.blocking_cells}, file_write)
            print('Map saved!')
