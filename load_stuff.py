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

from pygame import image

# TODO: This should come from another file (a file the map/game creator submits
# so that the program know all the images that can be used by the game.)
things_that_can_be = {'crop':1, 'grass':3, 'sand':7, 'water':8}
#things_that_can_be = ('crop', 'grass', 'sand', 'water')
creatures_that_can_be = ('hero', 'peasant', 'hunter-gatherers')

def images(number_of_layers, array):
    '''Looks what is on map then load the image files necessary to represent 
    them in the game. Returns a dictionary of all the images loaded.'''
    # TODO: This is CPU consuming because the for loops load an image each time
    # something is found in a cell, even if the image have already been loaded.
    # Make it check if it has been loaded so it doesn’t do it each time.
    images_loaded = {}
    for thing in things_that_can_be:
        for column in array:
            for cell in column:
                present_layer = 0
                while present_layer < number_of_layers: # “Less than”, because 
                # the number is correct: however, a list starts at 0
                    try:
                        if cell[present_layer] == things_that_can_be[thing]:
                            images_loaded[thing] = image.load(
                                    'art/{}.png'.format(thing))
                    except IndexError:
                        pass
                    present_layer += 1
    return images_loaded


def what_the_programmer_wants(images_loaded, thing_wanted):
    for iterable in (things_that_can_be,creatures_that_can_be):
        for thing in iterable:
            if thing == thing_wanted:
                images_loaded[thing] = image.load(
                        'art/{}.png'.format(thing))
    return images_loaded
