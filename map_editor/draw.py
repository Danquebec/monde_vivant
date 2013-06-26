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
from pygame.locals import *
from event import pixel_coords_of_thing

# As of now these two variables are only used in one function, but it could be
# nice to have zones adapt to the window size rather than be static.
WINDOW_SIZE_x = 1000 # Size of the screen
WINDOW_SIZE_y = 600 # Size of the screen

CELL_SIZE = 50

CELL_HOVER_RECT_COLOR = (0, 200, 0)
IMAGE_HOVER_RECT_COLOR = (255, 255, 50)
IMAGE_SELECTED_RECT_COLOR = (150, 50, 0)

EMPTY_RECT_THICKNESS = 3

def get_text_surfaces_and_rects(item, color, pos, font_obj):
    surface = font_obj.render(item, True, color)
    rect = surface.get_rect()
    rect.left, rect.top = pos
    return surface, rect


class Interface():
    '''Handles the preparation of the menu and it’s drawing, and the drawing of
    the zones (map zone and list of images zone) and of the map grid.'''
    def __init__(self, cells, CELL_SIZE):
        self.text_surfaces = []
        self.text_rects = []
        # The 0s are there because the two first text items are non 
        # selectables. TODO: Make this code better?
        self.text_selected_surfaces = [0, 0]
        self.text_selected_rects = [0, 0]
        self.text_greyed_surfaces = []
        self.text_greyed_rects = []
        self.Xs_surfaces = []
        self.Xs_rects = []
        self.Os_surfaces = []
        self.Os_rects = []
        self.map_rect = (10, 40, 600, 500)
        self.grid_rect = (10, 40, cells[0] * CELL_SIZE, cells[1] * CELL_SIZE)
        self.list_rect = ((self.map_rect[0] + self.map_rect[2] + 10), 40, 300,
                          500)
        self.grid_color = (40, 40, 40)
        self.map_rect_color = (150, 150, 120)
        self.list_rect_color = (100, 110, 120)

    def prepare_menu(self):
        '''It creates rects and surfaces for text that is not selected and 
        rects and surfaces for the layers selected.'''
        # TODO: This function seems to me as complicated… It could probably be
        # made simpler.
        font_obj = pygame.font.Font('freesansbold.ttf', 22)
        text_pos = [10, 9]
        normal_color = (50, 20, 220)
        selected_text_color = (220, 20, 20)
        greyed_text_color = (100, 100, 100)
        non_selectable_items = ['New', 'Save']
        mode_item = ['Blocking cells']
        selectable_items = ['layer0', 'layer1', 'layer2']
        for list_of_items in (non_selectable_items, mode_item,
                             selectable_items):
            for item in list_of_items:
                surface, rect = get_text_surfaces_and_rects(item, normal_color,
                                                            text_pos, font_obj)
                self.text_surfaces.append(surface)
                self.text_rects.append(rect)
                if (list_of_items == selectable_items or
                    list_of_items == mode_item):
                    selected_surface, selected_rect = \
                        get_text_surfaces_and_rects(
                        item, selected_text_color, text_pos, font_obj)
                    self.text_selected_surfaces.append(selected_surface)
                    self.text_selected_rects.append(selected_rect)
                if list_of_items == selectable_items:
                    greyed_surface, greyed_rect = \
                        get_text_surfaces_and_rects(
                        item, greyed_text_color, text_pos, font_obj)
                    self.text_greyed_surfaces.append(greyed_surface)
                    self.text_greyed_rects.append(greyed_rect)
                if list_of_items == non_selectable_items:
                    text_pos[0] += 80
                elif list_of_items == mode_item:
                    text_pos[0] += 180
                elif list_of_items == selectable_items:
                    text_pos[0] += 100

    def draw_menu(self, present_layer, is_blocking_cells_mode):
        '''Draws the menu items.'''
        if not is_blocking_cells_mode:
            if present_layer is not None: # So something is selected.
                for blit in range(6):
                    if blit == present_layer+3:
                        DISPLAYSURF.blit(self.text_selected_surfaces[blit],
                                         self.text_selected_rects[blit])
                    else:
                        DISPLAYSURF.blit(self.text_surfaces[blit],
                                         self.text_rects[blit])
            else:
                for blit in range(6):
                    DISPLAYSURF.blit(self.text_surfaces[blit],
                                     self.text_rects[blit])
        if is_blocking_cells_mode:
            for blit in range(2):
                DISPLAYSURF.blit(self.text_surfaces[blit],
                                 self.text_rects[blit])
            DISPLAYSURF.blit(self.text_selected_surfaces[2],
                             self.text_selected_rects[2])
            for blit in range(0, len(self.text_greyed_rects)):
                DISPLAYSURF.blit(self.text_greyed_surfaces[blit],
                                 self.text_greyed_rects[blit])

    def draw_zones(self):
        '''Draws the zones. Simple squares for the map and the list of
        images.'''
        pygame.draw.rect(DISPLAYSURF, self.map_rect_color, self.map_rect)
        pygame.draw.rect(DISPLAYSURF, self.list_rect_color, self.list_rect)
     
    def draw_grid(self, cells):
        '''Draws the map grid.'''
        posx = self.grid_rect[0]
        posy = self.grid_rect[1]
        endx = self.grid_rect[0] + (cells[0] * CELL_SIZE)
        endy = self.grid_rect[1] + (cells[1] * CELL_SIZE)
        # “end* + 1” to complete the grid with borders
        for x in range(posx, (endx + 1), CELL_SIZE):
            pygame.draw.line(DISPLAYSURF, self.grid_color, (x, posy),
                             (x, endy))
        for y in range(posy, (endy + 1), CELL_SIZE):
            pygame.draw.line(DISPLAYSURF, self.grid_color, (posx, y),
                             (endx, y))

    def prepare_Xs_and_Os(self, cells):
        self.Xs_surfaces = []
        self.Xs_rects = []
        self.Os_surfaces = []
        self.Os_rects = []
        font_obj = pygame.font.Font('freesansbold.ttf', 50)
        text_pos = [self.map_rect[0], self.map_rect[1]]
        color = (220, 220, 220)
        for column in xrange(cells[0]):
            text_pos[1] = self.map_rect[1]
            for cell in xrange(cells[1]):
                X_surface, X_rect = get_text_surfaces_and_rects('X', color, text_pos, font_obj)
                O_surface, O_rect = get_text_surfaces_and_rects('O', color, text_pos, font_obj)
                self.Xs_surfaces.append(X_surface)
                self.Xs_rects.append(X_rect)
                self.Os_surfaces.append(O_surface)
                self.Os_rects.append(O_rect)
                text_pos[1] += CELL_SIZE
            text_pos[0] += CELL_SIZE

    def draw_Xs_and_Os(self, is_blocking_cells_mode, array, cells):
        if is_blocking_cells_mode:
            i = 0
            for column in array:
                for cell in column:
                    if cell == 0:
                        DISPLAYSURF.blit(self.Os_surfaces[i], self.Os_rects[i])
                    elif cell == 1:
                        DISPLAYSURF.blit(self.Xs_surfaces[i], self.Xs_rects[i])
                    i += 1


def fill():
    '''Fills the screen with a grey background.'''
    DISPLAYSURF.fill((200, 200, 200))


def set_mode():
    '''Sets the mode.'''
    global DISPLAYSURF
    DISPLAYSURF = pygame.display.set_mode((WINDOW_SIZE_x, WINDOW_SIZE_y),
                                          HWSURFACE)


def images_list(images_loaded, list_rect, list_of_images):
    '''Draws the list of images in the interface that you can click to
    select.'''
    image_pos = [list_rect[0], list_rect[1]]
    for image in list_of_images:
        # TODO: make smaller than 50x50 px images blit centered.
        DISPLAYSURF.blit(images_loaded[image], (image_pos[0], image_pos[1]))
        image_pos[1] += CELL_SIZE


def define_color_of_empty_rect(what_color_for_empty_rect):
    '''Defines the color of the empty rect needed for a particular drawing
    function (an even function provides “what_color_for_empty_rect”). Empty 
    rects are used for hovering (help visual to see what your click is going to
    affect) and for selection (help visual to see what you selected).'''
    if what_color_for_empty_rect == 'cell hovered':
        color = CELL_HOVER_RECT_COLOR
    elif what_color_for_empty_rect == 'image hovered':
        color = IMAGE_HOVER_RECT_COLOR
    elif what_color_for_empty_rect == 'image selected':
        color = IMAGE_SELECTED_RECT_COLOR
    else:
        return (0, 0, 0)
    return color


def empty_rect(pos, color):
    '''Draws an empty rect. The position (“pos”) is provided by an event
    function. The color (“color”) is provided by the same function, by the 
    intermediary of the function “define_color_of_empty_rect” and of
    another drawing function (“hover_rect” or “selected_rect”).'''
    if pos:
        pygame.draw.rect(DISPLAYSURF, color, (pos[0], pos[1], CELL_SIZE,
                         CELL_SIZE), EMPTY_RECT_THICKNESS)


def hover_rect(pos, what_color_for_empty_rect):
    '''Draws an empty_rect for hovering. “pos” and “what_color_for_empty_rect”
    are provided by an event function managing items hovering.'''
    color = define_color_of_empty_rect(what_color_for_empty_rect)
    empty_rect(pos, color)


def selected_rect(pos):
    '''Draws an empty_rect for selection. “pos” and “what_color_for_empty_rect”
    are provided by an event function managing items selection.'''
    empty_rect(pos, IMAGE_SELECTED_RECT_COLOR)


def map_(array, images_loaded, list_of_images, map_rect, number_of_layers):
    '''Draws the map (“array”) with the images loaded (“images_loaded”, which
    needs “list_of_images” as an intermediary) on the map zone (“map_rect”).
    The number of layers is there to know how many times to iterate on the 
    map.'''
    for number in range(0, number_of_layers):
        column_number = 0
        for column in array:
            cell_number = 0
            for cell in column:
                for image in list_of_images:
                    if cell[number] == image:
                        pixel_coords = pixel_coords_of_thing(
                            (column_number, cell_number), map_rect, CELL_SIZE)
                        DISPLAYSURF.blit(images_loaded[image], pixel_coords)
                cell_number += 1
            column_number += 1
