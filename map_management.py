#!/usr/bin/python
# -*- coding:utf-8 -*-

# Monde vivant © 2013 Daniel Dumaresq
# e-mail: danquebec@singularity.fr
# Jabber: danquebec@linkmauve.fr

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

class map_():
    '''The class representing the map.'''
    def __init__(self):
        self.array = []
        self.number_of_layers = 0
        self.file_read = None
    def read(self):
        '''Creates the reader of a file, the 2D array from the file, finds
        thenumber_of_layers used on this map by looking the first cell of the
        map (array)'''
        self.file_read = open('map', 'rb')
        self.array = pickle.load(self.file_read)
        print(self.array)
        self.number_of_layers = len(self.array[0][0])