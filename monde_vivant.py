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
#import cProfile

import draw
import event
import load_stuff
from creatures import list_of_creatures
import map_management

FPS = 50

def main():
    '''Starting the program…'''
    global FPSCLOCK
    FPSCLOCK = pygame.time.Clock()
    
    mouse = (0, 0)
    mouse_down = False
    
    draw.set_mode()
    pygame.display.set_caption
    
    world = map_management.World()
    world.read() # TODO: Put that in the __init__…
    
    environment = event.Environment()
    
    # We load images here, so that they be loaded only once.
    start_load = time()
    images_loaded = load_stuff.images(world.number_of_layers, world.map)
    images_loaded = load_stuff.what_the_programmer_wants(
        images_loaded, 'hero')
    images_loaded = load_stuff.what_the_programmer_wants(images_loaded,
        'hunter-gatherers')
    images_loaded = load_stuff.what_the_programmer_wants(images_loaded,
        'crop')
    print(images_loaded)
    print('Time of loading:{}'.format(time() - start_load))

    hero = list_of_creatures[0]
    map_move = draw.move_camera(hero, world.map)

    main_loop(mouse, mouse_down, images_loaded, 
              world, map_move, hero, environment)


def main_loop(mouse, mouse_down, images_loaded, world,
              map_move, hero, environment, toward_where=False, tick_began=False,
              moving=False, action_call=False):
    '''The game loop.'''
    while True:
        mouse_clicked = False
        pressed_key = False
        
        # TODO: Something that allows the player to start changing direction
        # quickly (as of now, pressing an arrow key before stopping
        # pressing another arrow key doesn’t allow you to start moving in
        # this direction. You have to carefully remove your finger from the
        # the arrow key you were pressing before pressing another).
        if toward_where:
            hero.facing = toward_where
            # Trying to move…
            if not tick_began and not moving:
                # First foot…
                if hero.action is not None:
                    hero.action, hero.time_length = None, None
                    print('You interrupted your action.')
                if hero.foe is not None:
                    hero.foe = None
                    print('You interrupted your fight.')
                tick_began = time()
                moving = True
            
            # The next feet…
            if tick_began and moving:
                if time() - tick_began >= hero.speed:
                    hero.move(world.blocking_cells, toward_where,
                               list_of_creatures)
                    print(hero.pos)
                    tick_began = time() # c’était False
            
            # Handle the next feet after the second one…
            #if not tick_began and moving:
            #    tick_began = time()
        
        # Stop moving…
        if moving:
            if not toward_where:
                if time() - tick_began >= hero.speed:
                    tick_began = False
                    moving = False

        map_move = draw.move_camera(hero, world.map)
        
        draw.fill()
        draw.cells_on_lower_layers(images_loaded, world.number_of_layers, 
                world.map, load_stuff.things_that_can_be, map_move)
        draw.creatures(list_of_creatures, load_stuff.creatures_that_can_be, images_loaded, map_move, world.map)
        draw.cells_on_higher_layer(images_loaded, world.map, load_stuff.things_that_can_be, map_move)
        # draw.bottom_bar_zone()
        
        mouse, mouse_clicked, mouse_down, toward_where, pressed_key = event.handling(
            mouse, mouse_clicked, mouse_down, toward_where, pressed_key)
        
        if mouse_clicked:
            pass
            # event.get_cell_at_pixel(mouse[0], mouse[1], world.map, draw.CELLSIZE,
            #                        map_move)

        if pressed_key:
            if pressed_key == 't':
                action_call = hero.till_s()
            if pressed_key == 'a':
                hero.attack_s(list_of_creatures)
            if pressed_key == 'z':
                print(hero.facing)

        if hero.action:
            if time() - action_call >= hero.time_length:
                if hero.action == 'till':
                    hero.till_e(environment, world)

        if hero.foe:
            if time() - hero.last_hit >= hero.gear['strong hand'].speed:
                hero.attack_e()

        pygame.display.update()
        #print(FPSCLOCK.get_fps())
        FPSCLOCK.tick(FPS)


main()
