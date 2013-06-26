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

WINDOWSIZEx = 600 # Size of the screen
WINDOWSIZEy = 400 # Size of the screen

BOTTOMBARSIZEx = WINDOWSIZEx
BOTTOMBARSIZEy = 60
BOTTOMBARCOLOR = (101, 150, 200)

CELLSIZE = 50

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
                                    ((column_number*CELLSIZE)+map_move[0],
                                    (cell_number*CELLSIZE)+map_move[1]))
                            except pygame.error:
                                pygame.draw.rect(
                                    DISPLAYSURF, (0, 0, 0),
                                    ((column_number*CELLSIZE)+map_move[0],
                                    (cell_number*CELLSIZE)+map_move[1],
                                    CELLSIZE, CELLSIZE))
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
                                ((column_number*CELLSIZE)+map_move[0],
                                (cell_number*CELLSIZE)+map_move[1]))
                        except pygame.error:
                            pygame.draw.rect(
                                DISPLAYSURF, (0, 0, 0),
                                ((column_number*CELLSIZE)+map_move[0],
                                (cell_number*CELLSIZE)+map_move[1],
                                CELLSIZE, CELLSIZE))
                            # TODO: (0, 0, 0) should be a random color,
                            # instead.
                except IndexError:
                    pass
            cell_number += 1
        column_number += 1


def creatures(list_of_creatures, everything_that_can_be, images_loaded, map_move):
    for creature in list_of_creatures:
        for thing in everything_that_can_be:
            if creature.image == thing:
                try:
                    DISPLAYSURF.blit(images_loaded[thing], ((creature.pos[0]*CELLSIZE)+map_move[0], (creature.pos[1]*CELLSIZE)+map_move[1]))
                except pygame.error:
                    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), ((creature.pos[0]*CELLSIZE)+map_move[0], (creature.pos[1]*CELLSIZE)+map_move[1]))
                    # TODO: (0, 0, 0) should be a random color, instead.


def bottom_bar_zone():
    '''Mostly for test. Will definitely change.'''
    pygame.draw.rect(
        DISPLAYSURF, BOTTOMBARCOLOR, (0, (WINDOWSIZEy - BOTTOMBARSIZEy),
        BOTTOMBARSIZEx, BOTTOMBARSIZEy))
