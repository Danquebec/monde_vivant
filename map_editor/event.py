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

import pygame
import sys
from pygame.locals import *

def handling(mouse, mouse_clicked, mouse_down):
    '''Handles pygame events.'''
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
        elif event.type == KEYUP: # camera moving
            if event.key == K_RIGHT:
                pass
            elif event.key == K_LEFT:
                pass
            elif event.key == K_DOWN:
                pass
            elif event.key == K_UP:
                pass
    return mouse, mouse_clicked, mouse_down


def pixel_coords_of_thing(thing, rect, CELL_SIZE):
    '''Converts map or list coordinates to pixel coordinates. The “thing” is a 
    map column+cell or a rect, or anything with it’s x coordinate written in 
    [0] and y coordinate written in [1]. The “rect” is map or list zone, that 
    contains the “thing”.'''
    xmargin = rect[0]
    ymargin = rect[1]
    posx = thing[0] * CELL_SIZE + xmargin
    posy = thing[1] * CELL_SIZE + ymargin
    return (posx, posy)


def find_cell_at_pixel(mouse, map_rect, cells, CELL_SIZE, what_is_wanted):
    '''Find if the mouse is on a cell and on what cell.'''
    for cellx in range(cells[0]):
        for celly in range(cells[1]):
            pixel_coords = pixel_coords_of_thing((cellx, celly), map_rect,
                                                 CELL_SIZE)
            cell_rect = pygame.Rect(pixel_coords[0], pixel_coords[1],
                                    CELL_SIZE, CELL_SIZE)
            if cell_rect.collidepoint(mouse[0], mouse[1]):
                if what_is_wanted == 'cell':
                    return (cellx, celly)
                elif what_is_wanted == 'coords':
                    return pixel_coords, 'cell hovered'
                else:
                    raise Exception('what_is_wanted must be “cell” or '
                    '“coords.”. Got “{}” instead.'.format(what_is_wanted))
    if what_is_wanted is 'cell':
        return None
    elif what_is_wanted is 'coords':
        return None, None


def click_text_at_pixel(mouse, text_rects, is_cells_blocking_mode):
    '''Find if the mouse clicked on a menu item and what menu item.'''
    for rect in text_rects:
        if rect.collidepoint(mouse[0], mouse[1]):
            if rect == text_rects[0]:
                return 'new map'
            elif rect == text_rects[1]:
                return 'save map'
            elif rect == text_rects[2]:
                return 'blocking cells mode'
            else:
                if not is_cells_blocking_mode:
                    for position in range(3, len(text_rects)):
                        if rect == text_rects[position]:
                            return position - 3
    return None


def change_mode(is_blocking_cells_mode):
    if is_blocking_cells_mode:
        is_blocking_cells_mode = False
    elif not is_blocking_cells_mode:
        is_blocking_cells_mode = True
    return is_blocking_cells_mode


def get_map_size_input():
    '''Get the desired size of the map, or more presicely, the number of cells
    on x and y desired, which is entered by the user.'''
    def get_value_input(desired_value):
        while True:
            try:
                value = int(raw_input('cells on {}\n> '.format(desired_value)))
            except ValueError:
                value = 0
            if value < 2:
                print('The number of cells on each side must be at least 2!')
            elif value >= 2:
                return value
    x = get_value_input('x')
    y = get_value_input('y')
    cells = (x, y)
    return cells


def find_image_at_pixel(mouse, list_rect, list_of_images, CELL_SIZE,
                        what_is_wanted):
    '''Find if the mouse is on an image in the list of selectable images and on
    what image.'''
    image_pos = [list_rect[0], list_rect[1]]
    for image in list_of_images:
        image_rect = pygame.Rect(image_pos[0], image_pos[1], CELL_SIZE,
                                 CELL_SIZE)
        if image_rect.collidepoint(mouse[0], mouse[1]):
            if what_is_wanted == 'pos and image':
                return image_pos, image
            elif what_is_wanted == 'pos only':
                return image_pos, 'image hovered'
            else:
                raise Exception('what_is_wanted must be “pos and image” or '
                '“pos only”. Got “{}” instead.'.format(what_is_wanted))
        image_pos[1] += CELL_SIZE
    return None, (0, 0, 0)


class ImageSelected():
    '''Handles the image selected (of the list of images, which you can then
    put in the map.'''
    def __init__(self):
        self.image_selected = None
        self.rect_pos = None
    def click_image_at_pixel(self, mouse, list_rect, list_of_images,
                             CELL_SIZE):
        '''Click an image in the list of images.'''
        pos, image_selected = find_image_at_pixel(
            mouse, list_rect,list_of_images, CELL_SIZE, 'pos and image')
        if pos:
            print(image_selected)
            self.image_selected = image_selected
            self.rect_pos = pos
            return 'image selected'
