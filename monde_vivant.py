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
    images_loaded = load_stuff.images(map_.number_of_layers, map_.map)
    images_loaded = load_stuff.what_the_programmer_wants(
        images_loaded, 'heros')
    images_loaded = load_stuff.what_the_programmer_wants(images_loaded,
        'hunter-gatherers')

    heros = list_of_creatures[0]
    map_move = draw.move_camera(heros, map_.map)

    main_loop(mouse, mouse_down, images_loaded, map_.number_of_layers,
              map_.map, map_.blocking_cells, map_move, heros)


def main_loop(mouse, mouse_down, images_loaded, number_of_layers, array, blocking_cells_map,
              map_move, heros, toward_where=False, tick_began=False,
              moving=False):
    '''The game loop.'''
    while True:
        mouse_clicked = False
        
        # TODO: Something that allows the player to start changing direction
        # quickly (as of now, pressing an arrow key before stopping
        # pressing another arrow key doesn’t allow you to start moving in
        # this direction. You have to carefully remove your finger from the
        # the arrow key you were pressing before pressing another).
        if toward_where:
            # Trying to move…
            if not tick_began and not moving:
                # First foot…
                heros.move(blocking_cells_map, toward_where, list_of_creatures)
                print(heros.pos)
                tick_began = time()
                moving = True
            
            # The next feet…
            if tick_began and moving:
                if time() - tick_began >= heros.speed:
                    heros.move(blocking_cells_map, toward_where,
                               list_of_creatures)
                    print(heros.pos)
                    tick_began = False
            
            # Handle the next feet after the second one…
            if not tick_began and moving:
                tick_began = time()
        
        # Stop moving…
        if moving:
            if not toward_where:
                if time() - tick_began >= heros.speed:
                    tick_began = False
                    moving = False
        
        map_move = draw.move_camera(heros, array)
        
        #slide_to, map_move = event.slide_to(slide_to, map_move, draw.CELLSIZE)
        
        draw.fill()
        draw.cells_on_lower_layers(images_loaded, number_of_layers, array,
                   load_stuff.everything_that_can_be, map_move)
        draw.creatures(list_of_creatures, load_stuff.everything_that_can_be, images_loaded, map_move, array)
        draw.cells_on_higher_layer(images_loaded, array, load_stuff.everything_that_can_be, map_move)
        # draw.bottom_bar_zone()
        
        mouse, mouse_clicked, mouse_down, toward_where = event.handling(
            mouse, mouse_clicked, mouse_down, toward_where)
        
        if mouse_clicked:
            event.get_cell_at_pixel(mouse[0], mouse[1], array, draw.CELLSIZE,
                                    map_move)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

main()
