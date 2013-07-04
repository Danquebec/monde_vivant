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

CELL_SIZE = 50

WINDOWSIZEx = 11 * CELL_SIZE # Size of the screen
WINDOWSIZEy = 11 * CELL_SIZE # Size of the screen

BOTTOMBARSIZEx = WINDOWSIZEx
BOTTOMBARSIZEy = 60
BOTTOMBARCOLOR = (101, 150, 200)



def set_mode():
    '''Sets the mode.'''
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEx, WINDOWSIZEy),
                                          HWSURFACE)


def fill():
    DISPLAYSURF.fill((0, 0, 0))


def cells_on_lower_layers(images_loaded, number_of_layers, array, everything_that_can_be,
          map_move):
    '''Draws all the cells on the layers lower than the creatures.'''
    for number in range(0, number_of_layers-1): # Hum… This was at 4 before… Why. How.
        column_number = 0
        for column in array:
            cell_number = 0
            for cell in column:
                for thing in everything_that_can_be:
                    try:
                        if cell[number] == thing:
                            try:
                                DISPLAYSURF.blit(
                                    images_loaded[thing],
                                    ((column_number*CELL_SIZE)-map_move[0],
                                    (cell_number*CELL_SIZE)-map_move[1]))
                            except pygame.error:
                                pygame.draw.rect(
                                    DISPLAYSURF, (0, 0, 0),
                                    ((column_number*CELL_SIZE)-map_move[0],
                                    (cell_number*CELL_SIZE)-map_move[1],
                                    CELL_SIZE, CELL_SIZE))
                                # TODO: (0, 0, 0) should be a random color,
                                # instead.
                    except IndexError:
                        pass
                cell_number += 1
            column_number += 1


def cells_on_higher_layer(images_loaded, array, everything_that_can_be, map_move):
    '''Draws the cells on the layer higher than the creatures.'''
    column_number = 0
    for column in array:
        cell_number = 0
        for cell in column:
            for thing in everything_that_can_be:
                try:
                    if cell[2] == thing:
                        try:
                            DISPLAYSURF.blit(
                                images_loaded[thing],
                                ((column_number*CELL_SIZE)-map_move[0],
                                (cell_number*CELL_SIZE)-map_move[1]))
                        except pygame.error:
                            pygame.draw.rect(
                                DISPLAYSURF, (0, 0, 0),
                                ((column_number*CELL_SIZE)-map_move[0],
                                (cell_number*CELL_SIZE)-map_move[1],
                                CELL_SIZE, CELL_SIZE))
                            # TODO: (0, 0, 0) should be a random color,
                            # instead.
                except IndexError:
                    pass
            cell_number += 1
        column_number += 1

MARGIN = 5

def creatures(list_of_creatures, everything_that_can_be, images_loaded, map_move, array):
    def put_heros_at_right_place(heros, axis, cells):
        #print(cells)
        if heros.pos[axis] <= MARGIN:
            screen_pos = heros.pos[axis]
        elif heros.pos[axis] > MARGIN and heros.pos[axis] <= cells - MARGIN:
            screen_pos = 5
        elif heros.pos[axis] > cells - MARGIN:
            screen_pos = heros.pos[axis] - (cells - (MARGIN * 2))
        return screen_pos
    for creature in list_of_creatures:
        for thing in everything_that_can_be:
            if creature == list_of_creatures[0]: # if it’s the heros
                if creature.image == thing:
                    screen_pos = [put_heros_at_right_place(list_of_creatures[0], 0, len(array)), put_heros_at_right_place(list_of_creatures[0], 1, len(array[0]))]
                    try:
                        DISPLAYSURF.blit(images_loaded[thing], ((screen_pos[0]*CELL_SIZE), (screen_pos[1]*CELL_SIZE)))
                    except pygame.error:
                        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), ((screen_pos[0]*CELL_SIZE), (screen_pos[1]*CELL_SIZE)))
                        # TODO: (0, 0, 0) should be a random color, instead.
            
            else:
                if creature.image == thing:
                    try:
                        DISPLAYSURF.blit(images_loaded[thing], ((creature.pos[0]*CELL_SIZE)-map_move[0], (creature.pos[1]*CELL_SIZE)-map_move[1]))
                    except pygame.error:
                        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), ((creature.pos[0]*CELL_SIZE)-map_move[0], (creature.pos[1]*CELL_SIZE)-map_move[1]))
                        # TODO: (0, 0, 0) should be a random color, instead.

'''
def bottom_bar_zone():
    pygame.draw.rect(
        DISPLAYSURF, BOTTOMBARCOLOR, (0, (WINDOWSIZEy - BOTTOMBARSIZEy),
        BOTTOMBARSIZEx, BOTTOMBARSIZEy))
'''

def move_camera(heros, array):
    def move_camera_on_both_axis(heros, cells, axis):
        if heros.pos[axis] <= MARGIN:
            map_move = 0
        elif heros.pos[axis] > MARGIN and heros.pos[axis] <= cells - MARGIN:
            map_move = (heros.pos[axis] - MARGIN) * CELL_SIZE
        elif heros.pos[axis] > cells - MARGIN:
            map_move = (cells - (MARGIN * 2)) * CELL_SIZE
        return map_move
    map_move = [move_camera_on_both_axis(heros, len(array), 0), move_camera_on_both_axis(heros, len(array[0]), 1)]
    return map_move
