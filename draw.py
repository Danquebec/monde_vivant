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

import pygame
from pygame.locals import *

CELL_SIZE = 32

WINDOWSIZEx = 10 * CELL_SIZE # Size of the screen
WINDOWSIZEy = 10 * CELL_SIZE # Size of the screen

BOTTOMBARSIZEx = WINDOWSIZEx
BOTTOMBARSIZEy = 60
BOTTOMBARCOLOR = (101, 150, 200)


class Drawable(object):
    def __init__(self):
        self.image = image

    def draw(self):
        pass

'''
class InventoryInterface(object): # Ouais, pénis.
    def prepare_inventory_interface(self):
        font_obj = pygame.font.Font('freesansbold.ttf', 15)
        text_pos = [WINDOWSIZEx - 100, 5]
'''

def set_mode():
    '''Sets the mode.'''
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEx, WINDOWSIZEy),
                                          HWSURFACE)


def fill():
    DISPLAYSURF.fill((0, 0, 0))


def cells_on_lower_layers(images_loaded, number_of_layers, array,
                          things_that_can_be, map_move, hero):
    '''Draws all the cells on the layers lower than the creatures.'''
    for layer in xrange(0, number_of_layers-1):
        for x in xrange(hero.pos[0]-5, hero.pos[0]+5):
            for y in xrange(hero.pos[1]-5, hero.pos[1]+5):
                for thing in things_that_can_be:
                    try:
                        if array[x][y][layer] == things_that_can_be[thing]:
                            DISPLAYSURF.blit(images_loaded[thing],
                                             ((x*CELL_SIZE)-map_move[0],
                                             (y*CELL_SIZE)-map_move[1]))
                    except IndexError:
                        pass
    '''
    for number in range(0, number_of_layers-1): # Hum… This was at 4 before… Why. How.
        column_number = 0
        for column in array:
            cell_number = 0
            for cell in column:
                for thing in things_that_can_be:
                    try:
                        if cell[number] == things_that_can_be[thing]:
                            DISPLAYSURF.blit(
                                    images_loaded[thing],
                                    ((column_number*CELL_SIZE)-map_move[0],
                                    (cell_number*CELL_SIZE)-map_move[1]))
                    except IndexError:
                        pass
                cell_number += 1
            column_number += 1
    '''


def cells_on_higher_layer(images_loaded, array, things_that_can_be, map_move,
                          hero):
    '''Draws the cells on the layer higher than the creatures.'''
    for x in xrange(hero.pos[0]-5, hero.pos[0]+5):
        for y in xrange(hero.pos[1]-5, hero.pos[1]+5):
            for thing in things_that_can_be:
                try:
                    if array[x][y][2] == things_that_can_be[thing]:
                        DISPLAYSURF.blit(images_loaded[thing],
                                         ((x*CELL_SIZE)-map_move[0],
                                         (y*CELL_SIZE)-map_move[1]))
                except IndexError:
                    pass
'''
    column_number = 0
    for column in array:
        cell_number = 0
        for cell in column:
            for thing in things_that_can_be:
                try:
                    if cell[2] == things_that_can_be[thing]:
                        DISPLAYSURF.blit(
                                images_loaded[thing],
                                ((column_number*CELL_SIZE)-map_move[0],
                                (cell_number*CELL_SIZE)-map_move[1]))
                except IndexError:
                    pass
            cell_number += 1
        column_number += 1
'''

MARGIN = 5

def creatures(list_of_creatures, creatures_that_can_be, images_loaded, map_move, array):
    def put_hero_at_right_place(hero, axis, cells):
        #print(cells)
        if hero.pos[axis] <= MARGIN:
            screen_pos = hero.pos[axis]
        elif hero.pos[axis] > MARGIN and hero.pos[axis] <= cells - MARGIN:
            screen_pos = 5
        elif hero.pos[axis] > cells - MARGIN:
            screen_pos = hero.pos[axis] - (cells - (MARGIN * 2))
        return screen_pos
    for creature in list_of_creatures:
        for thing in creatures_that_can_be:
            if creature == list_of_creatures[0]: # if it’s the hero
                if creature.image == thing:
                    screen_pos = [put_hero_at_right_place(list_of_creatures[0], 0, len(array)), put_hero_at_right_place(list_of_creatures[0], 1, len(array[0]))]
                    DISPLAYSURF.blit(images_loaded[thing], ((screen_pos[0]*CELL_SIZE), (screen_pos[1]*CELL_SIZE)))
            
            else:
                if creature.image == thing:
                    DISPLAYSURF.blit(images_loaded[thing], ((creature.pos[0]*CELL_SIZE)-map_move[0], (creature.pos[1]*CELL_SIZE)-map_move[1]))

'''
def bottom_bar_zone():
    pygame.draw.rect(
        DISPLAYSURF, BOTTOMBARCOLOR, (0, (WINDOWSIZEy - BOTTOMBARSIZEy),
        BOTTOMBARSIZEx, BOTTOMBARSIZEy))
'''

def move_camera(hero, array):
    def move_camera_on_both_axis(hero, cells, axis):
        if hero.pos[axis] <= MARGIN:
            map_move = 0
        elif hero.pos[axis] > MARGIN and hero.pos[axis] <= cells - MARGIN:
            map_move = (hero.pos[axis] - MARGIN) * CELL_SIZE
        elif hero.pos[axis] > cells - MARGIN:
            map_move = (cells - (MARGIN * 2)) * CELL_SIZE
        return map_move
    map_move = [move_camera_on_both_axis(hero, len(array), 0), move_camera_on_both_axis(hero, len(array[0]), 1)]
    return map_move

