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
import sys
from pygame.locals import *

class Environment(object):
    '''Takes notes of everything of importance on the map, like the crops,
    the time left for wheat plantations to mature, etc. Also contains functions
    that modify the environment (e.g. a peasant tills, so it adds a crop…).'''
    def __init__(self, crops=[], junk=[]):
        self.crops = crops
        self.junk = junk
    crop_duration = 100
    wheat_growth_time = 30 # 30 in-game days, or, 12 hours in our world.
    soft_junk_duration = 3
    hard_junk_duration = 10 * 365
    soft_junk_types = ('seeds', 'plant')
    hard_junk_types = ('hoe', 'sickle')
    class Crop(object):
        def __init__(self, pos, created, what_seeded,
                     when_seeded, growth_level):
            self.pos = pos
            self.created = created
            self.what_seeded = what_seeded
            self.when_seeded = when_seeded
            self.growth_level = growth_level
        def seed(self, seeds, day, world):
            if self.what_seeded is None:
                self.what_seeded = seeds
                self.when_seeded = day
                self.growth_level = 0
                if seeds == 'wheat seeds':
                    world.modify(1, 10, self.pos)
        def harvest(self, world):
            if self.growth_level == 2 or self.growth_level == 1:
                self.what_seeded, self.when_seeded = None, None
                self.growth_level = 0
                world.modify(0, 3, self.pos)
                world.modify(1, 0, self.pos)
                world.modify(2, 0, [self.pos[0], self.pos[1]-1])
            elif self.growth_level == 0:
                pass

    class Junk(object):
        '''Random stuff on ground, weapons dropped, etc.'''
        def __init__(self, what, pos, when_dropped):
            self.what = what
            self.pos = pos
            self.when_dropped = when_dropped

    def add_crop(self, world, pos, day):
        if self.crops is None:
            self.crops = []
        for crop in self.crops:
            if crop.pos == pos:
                return
        world.modify(0, 1, pos) # 1 for “crop”
        self.crops.append(self.Crop(pos, day, None, None, None))

    def check_crops(self, day, world):
        crop_number = 0
        for crop in self.crops:
            if not crop.what_seeded or crop.growth_level == 2:
                if (day - crop.created >= self.crop_duration):
                    self.crops.pop(crop_number)
                    world.modify(0, 3, crop.pos)
                    world.modify(1, 0, crop.pos)
                    world.modify(2, 0, [crop.pos[0], crop.pos[1]-1])
            elif crop.what_seeded == 'wheat seeds':
                if day - crop.when_seeded >= self.wheat_growth_time:
                    crop.growth_level = 2
                    world.modify(1, 13, crop.pos)
                    world.modify(2, 14, [crop.pos[0], crop.pos[1]-1])
                elif day - crop.when_seeded >= self.wheat_growth_time / 2:
                    crop.growth_level = 1
                    world.modify(1, 11, crop.pos)
                    world.modify(2, 12, [crop.pos[0], crop.pos[1]-1])
            crop_number += 1
'''  
    def check_junk(self, day, world):
        junk_number = 0
        for thing in self.junk:
            for soft_junk in self.soft_junk_types:
                if thing.type_ == soft_junk:
                    if day >= soft_junk_duration:
                        world.modify(1, 0, thing.pos)
                        self.junk.pop(junk_number)
            for hard_junk in self.hard_junk_types:
                if thing.type_ == hard_junk:
                    if day >= hard_junk_duration:
                        world.modify(1, 0, junk.pos) # Bleh pénis
                        self.junk.pop(junk_number) # Années, jour remis à 0
                        # peut pas compter en jours :(:(
                        # prendre en compte son self.dropped ……
                        # changer la carte et faire des strings
                    if thing.__class__.__name__ == 'WieldableObject':
                        if day >= hard_junk_duration
    
    def take_junk(self,
'''

class Time(object):
    '''Manages years, months, weeks, days, nights, etc.'''
    def __init__(self, starting_point):
        self.starting_point = starting_point
        self.year = 0
        self.month = 0
        self.week = 0
        self.day = 0
        self.hour = 0
    hour_c =  60*60.0 # one minute in our world
    day_c =   24      # hours. 24 minutes in our world
    week_c =  7       # days. nearly three hours in our world
    month_c = 30      # days. 12 hours in our world
    year_c =  12      # months. 146 hours, or 2 months playing 2 hours a day,
                      # in our world
    def check(self, time):
        h, d, m, y = False, False, False, False # is it a new X?
        if time - self.starting_point >= self.hour_c:
            self.hour += 1
            self.starting_point = time
            h = True
            if self.hour >= day_c:
                self.day += 1
                self.hour = 0
                d = True
                # TODO continue…
        if h:
            if d:
                if m:
                    if y:
                        print('A new year has begun. '
                              'We are now at year {}.'.format(self.year))
                    else:
                        print('We are now at month {}, '
                              'of year {}'.format(self.month, self.year))
                else:
                    print('We are now at day {}, of month {}, of year {},'
                          'and it is day {} of '
                          'week {}.'.format(self.day, self.month, self.year,
                                            self.day, self.week))
                    return 'new day'
            else:
                print('We are now at {} hour.'.format(self.hour))
    def jump_a_day(self):
        self.day += 1
        print('Day {}.'.format(self.day))

def handling(mouse, mouse_clicked, mouse_down, toward_where, pressed_key):
    '''Handles every event. It returns the updates of the mouse position and of
    the state of the mouse (did it click? is the mouse pressed?).'''
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mouse = event.pos
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_clicked = True
                mouse_down = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                mouse_down = False
            mousex, mousey = event.pos
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                toward_where = 'right'
            elif event.key == K_LEFT:
                toward_where = 'left'
            elif event.key == K_DOWN:
                toward_where = 'down'
            elif event.key == K_UP:
                toward_where = 'up'
            elif event.key == K_0:
                print('vagin')
        elif event.type == KEYUP:
            if event.key == K_t:
                pressed_key = 't'
            elif event.key == K_a:
                pressed_key = 'a'
            elif event.key == K_e:
                pressed_key = 'e'
            elif event.key == K_i:
                pressed_key = 'i'
            elif event.key == K_p:
                pressed_key = 'p'
            elif event.key == K_s:
                pressed_key = 's'
            elif event.key == K_w:
                pressed_key = 'w'
            elif event.key == K_v:
                pressed_key = 'v'
            elif event.key == K_z:
                pressed_key = 'z' # this is for tests
            elif event.key == 42: # K_0 qwerty
                pressed_key = 0
            elif event.key == 34: # K_1 qwerty
                pressed_key = 1
            elif event.key == 171: # K_2 qwerty
                pressed_key = 2
            elif event.key == 187: # K_3 qwerty
                pressed_key = 3
            toward_where = False
    return mouse, mouse_clicked, mouse_down, toward_where, pressed_key


def get_cell_at_pixel(x, y, array, CELLSIZE, map_move):
    '''When the mouse clicks, it finds what was clicked. Should return 
    something in the future. For now, it prints what it clicked, for test
    purposes.'''
    column_number = 0
    for column in array:
        cell_number = 0
        for cell in column:
            left = column_number*CELLSIZE + map_move[0]
            top = cell_number*CELLSIZE + map_move[1]
            box_rect = pygame.Rect(left, top, CELLSIZE, CELLSIZE)
            if box_rect.collidepoint(x, y):
                print(cell)
            cell_number += 1
        column_number += 1
