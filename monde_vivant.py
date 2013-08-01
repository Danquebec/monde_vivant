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
# list_of_creatures[0] is the hero

import pygame
from time import time

import draw
import event
import load_stuff
from creatures import list_of_creatures
from creatures import wheat_seeds
import map_management

FPS = 40

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
    world_time = event.Time(time())
    keys = {'p': False, # Planting Seeds Mode.
            'e': False} # Equip

    # We load images here, so that they be loaded only once.
    start_load = time()
    images_loaded = load_stuff.images(world.number_of_layers, world.map)
    images_loaded = load_stuff.what_the_programmer_wants(
        images_loaded, 'hero')
    images_loaded = load_stuff.what_the_programmer_wants(images_loaded,
        'peasant')
    images_loaded = load_stuff.what_the_programmer_wants(images_loaded,
        'wheat0')
    images_loaded = load_stuff.what_the_programmer_wants(images_loaded,
        'wheat1')
    images_loaded = load_stuff.what_the_programmer_wants(images_loaded,
        'wheat1_top')
    images_loaded = load_stuff.what_the_programmer_wants(images_loaded,
        'wheat2')
    images_loaded = load_stuff.what_the_programmer_wants(images_loaded,
        'wheat2_top')
    images_loaded = load_stuff.what_the_programmer_wants(images_loaded,
        'crop')
    print(images_loaded)
    print('Time of loading:{}'.format(time() - start_load))

    map_move = draw.move_camera(list_of_creatures[0], world.map)

    main_loop(mouse, mouse_down, images_loaded, world_time,
              world, keys, map_move, environment)


def main_loop(mouse, mouse_down, images_loaded, world_time, world, keys,
              map_move, environment, toward_where=False, tick=False,
              moving=False, action_call=False):
    '''The game loop.'''
    while True:
        mouse_clicked = False
        pressed_key = None

        # TODO: Something that allows the player to start changing direction
        # quickly (as of now, pressing an arrow key before stopping
        # pressing another arrow key doesn’t allow you to start moving in
        # this direction. You have to carefully remove your finger from the
        # the arrow key you were pressing before pressing another).
        for creature in list_of_creatures:
            if creature.toward_where:
                creature.facing = creature.toward_where
                if not creature.tick and not creature.moving:
                    creature.first_foot(world.blocking_cells, 
                                        list_of_creatures)
                if creature.tick and creature.moving:
                    creature.next_feet(world.blocking_cells, list_of_creatures)
            if creature.moving:
                if not creature.toward_where:
                    if time() - creature.tick >= creature.speed:
                        creature.tick = False
                        creature.moving = False
        '''
        if toward_where:
            list_of_creatures[0].facing = toward_where
            # Trying to move…
            if not tick and not moving:
                # First foot…
                if list_of_creatures[0].action is not None:
                    list_of_creatures[0].action, list_of_creatures[0].time_length = None, None
                    print('You interrupted your action.')
                if list_of_creatures[0].foe is not None:
                    list_of_creatures[0].foe = None
                    print('You interrupted your fight.')
                tick = time()
                moving = True

            # The next feet…
            if tick and moving:
                if time() - tick >= list_of_creatures[0].speed:
                    list_of_creatures[0].move(world.blocking_cells, toward_where,
                               list_of_creatures)
                    print(list_of_creatures[0].pos)
                    tick = time() # c’était False

            # Handle the next feet after the second one…
            #if not tick and moving:
            #    tick = time()

        # Stop moving…
        if moving:
            if not toward_where:
                if time() - tick >= list_of_creatures[0].speed:
                    tick = False
                    moving = False
        '''

        map_move = draw.move_camera(list_of_creatures[0], world.map)

        draw.fill()
        draw.cells_on_lower_layers(images_loaded, world.number_of_layers, 
                world.map, load_stuff.things_that_can_be, map_move, list_of_creatures[0])
        draw.creatures(list_of_creatures, load_stuff.creatures_that_can_be, images_loaded, map_move, world.map)
        draw.cells_on_higher_layer(images_loaded, world.map, load_stuff.things_that_can_be, map_move, list_of_creatures[0])
        # draw.bottom_bar_zone()

        mouse, mouse_clicked, mouse_down, list_of_creatures[0].toward_where, pressed_key = event.handling(
            mouse, mouse_clicked, mouse_down, list_of_creatures[0].toward_where, pressed_key)
        #print(pressed_key)

        if mouse_clicked:
            pass
            # event.get_cell_at_pixel(mouse[0], mouse[1], world.map, draw.CELLSIZE,
            #                        map_move)

        if pressed_key is not None:
            if pressed_key == 't':
                action_call = list_of_creatures[0].till_s()
            elif pressed_key == 'a':
                list_of_creatures[0].attack_s(list_of_creatures)
            elif pressed_key == 'p':
                if keys['p'] == False:
                    keys['p'] = True
                    print('You are now in Planting Seeds Mode')
                else:
                    keys['p'] = False
                    print('You are now in normal mode')
            elif pressed_key == 'w':
                if keys['p'] == True:
                    list_of_creatures[0].plant(
                            wheat_seeds, world_time.day, environment, world)
            elif pressed_key == 'e':
                if keys['e']:
                    keys['e'] = False
                    print('Equipping canceled')
                elif keys['e'] is False:
                    keys['e'] = True
                    print('You are now trying to equip something')
            elif pressed_key == 's':
                if keys['e'] is True:
                    try:
                        list_of_creatures[0].gear['back pack'].list_content(
                                'WieldableObject')
                        keys['e'] = 's'
                    except AttributeError:
                        print('You need a back pack to list content.')
            elif pressed_key == 0:
                if keys['e'] == 's':
                    list_of_creatures[0].equip(0)
                    keys['e'] = False
            elif pressed_key == 1:
                if keys['e'] == 's':
                    list_of_creatures[0].equip(1)
                    keys['e'] = False
            elif pressed_key == 2:
                if keys['e'] == 's':
                    list_of_creatures[0].equip(2)
                    keys['e'] = False
            elif pressed_key == 3:
                if keys['e'] == 's':
                    list_of_creatures[0].equip(3)
                    keys['e'] = False
            elif pressed_key == 'z': # this is for tests
                world_time.jump_a_day()
                environment.check_crops(world_time.day, world)

        for creature in list_of_creatures:
            if creature.action:
                if time() - action_call >= creature.time_length:
                    if creature.action == 'till':
                        creature.till_e(environment, world, world_time.day)

            if creature.foe:
                if time() - creature.last_hit >= list_of_creatures[0].gear['strong hand'].speed:
                    creature.attack_e()

        new_X = world_time.check(time())
        if new_X:
            if new_X == 'new day':
                environment.check_crops(world_time.day, world)

        pygame.display.update()
        #print(FPSCLOCK.get_fps())
        FPSCLOCK.tick(FPS)


main()
