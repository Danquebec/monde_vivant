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

# The variable “mouse” is the position of the mouse cursor.

import pygame
from time import time

import draw
import event
import load_stuff
from creatures import list_of_creatures
import map_management

FPS = 30

def main():
    '''Starting the program…'''
    global FPSCLOCK
    FPSCLOCK = pygame.time.Clock()
    
    mouse = (0, 0)
    mouse_down = False
    
    draw.set_mode()
    pygame.display.set_caption
    
    map_ = map_management.map_()
    map_.read()
    
    # We load images here, so that they be loaded only once.
    images_loaded = load_stuff.images(map_.number_of_layers, map_.array)
    
    map_move = [0, 0]
    
    heros = list_of_creatures[0]

    main_loop(mouse, mouse_down, images_loaded, map_.number_of_layers,
              map_.array, map_move, heros)


def main_loop(mouse, mouse_down, images_loaded, number_of_layers, array,
              map_move, heros, toward_where=False, tick_began=False):
    '''The game loop.'''
    while True:
        mouse_clicked = False
        
        if not toward_where:
            is_moving = False
        
        if toward_where and not tick_began and is_moving:
            tick_began = time()
        
        if toward_where and not is_moving:
            heros.move(toward_where)
            tick_began = time()
            is_moving = True
        
        if tick_began:
            if time() - tick_began >= heros.speed:
                heros.move(toward_where)
                print(heros.pos)
                tick_began = False
        
        #slide_to, map_move = event.slide_to(slide_to, map_move, draw.CELLSIZE)
        
        draw.fill()
        draw.cells(images_loaded, number_of_layers, array,
                   load_stuff.everything_that_can_be, map_move)
        draw.bottom_bar_zone()
        
        mouse, mouse_clicked, mouse_down, toward_where = event.handling(
            mouse, mouse_clicked, mouse_down, toward_where)
        
        if mouse_clicked:
            event.get_cell_at_pixel(mouse[0], mouse[1], array, draw.CELLSIZE,
                                    map_move)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

main()
