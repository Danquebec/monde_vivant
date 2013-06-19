#!/usr/bin/python
# -*- coding:utf-8 -*-

# Monde vivant’s map editor © 2013 Daniel Dumaresq
# e-mail: danquebec@singularity.fr
# Jabber: danquebec@linkmauve.org

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

from os import listdir
from pygame import image as p_image

def images():
    '''Load all the images in the “art” folder.'''
    images_loaded = {}
    list_of_images = [f for f in listdir('../art/') if f[-4:] == '.png']
    new_list_of_images = []
    list_of_images.sort()
    for image in list_of_images:
        image = list(image)
        for pop in range(4):
            # remove the .png from each item of the list, to be used later.
            image.pop()
        image = ''.join(image)
        new_list_of_images.append(image)
        images_loaded[image] = p_image.load('../art/{}.png'.format(image))
    list_of_images = new_list_of_images
    return images_loaded, list_of_images
