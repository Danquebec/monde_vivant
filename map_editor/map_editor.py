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

# Many tuples will be like this: (10, 25). This means that the first number is
# x, and the other is y. So rectangle_pos[0] is the x position of the rectangle
# and rectangle_pos[1] is its y position.

import pygame

import draw
import load_stuff
import event
import make_map

FPS = 30

def main():
    '''Start the program…'''
    global FPSCLOCK
    FPSCLOCK = pygame.time.Clock()
    
    mouse = (0, 0)
    
    hover_rect_pos = None
    map_began = False
    what_is_clicked = None
    present_layer = None
    cell = None
    mouse_down = False
    cells = (0, 0)
    what_color_for_empty_rect = (0, 0, 0)
    
    pygame.init()

    draw.set_mode()
    pygame.display.set_caption('Map editor')
    
    # list_of_images will be useful to know what image is selected when the 
    # user clicks on an image
    images_loaded, list_of_images = load_stuff.images()
    
    interface = draw.Interface(cells, draw.CELL_SIZE)
    interface.prepare_menu()
    image_selected = event.ImageSelected()
    map_ = make_map.Map()

    main_loop(mouse, images_loaded, cells, hover_rect_pos, map_began, 
              list_of_images, image_selected, what_is_clicked, present_layer, 
              cell, mouse_down, map_, interface, what_color_for_empty_rect)


def main_loop(mouse, images_loaded, cells, hover_rect_pos, map_began, 
              list_of_images, image_selected, what_is_clicked, present_layer,
              cell, mouse_down, map_, interface, what_color_for_empty_rect):
    '''The main loop.'''
    while True:
        mouse_clicked = False

        draw.fill()
        interface.draw_menu(present_layer)
        interface.draw_zones()
        draw.images_list(images_loaded, interface.list_rect, list_of_images)
        interface.draw_grid(cells)   
        draw.selected_rect(image_selected.rect_pos)
        if map_.array:
            draw.map_(map_.array, images_loaded, list_of_images, 
                      interface.map_rect, map_.number_of_layers)
        draw.hover_rect(hover_rect_pos, what_color_for_empty_rect)
        
        
        mouse, mouse_clicked, mouse_down = event.handling(mouse, mouse_clicked,
                                                          mouse_down)

        hover_rect_pos, what_color_for_empty_rect = event.find_cell_at_pixel(
            mouse, interface.map_rect, cells, draw.CELL_SIZE, 'coords')
        if hover_rect_pos is None: 
        # If you’re not hovering a cell on map, then maybe are you hovering an
        # image in the list of images.
            hover_rect_pos, what_color_for_empty_rect = \
                event.find_image_at_pixel(
                mouse, interface.list_rect, list_of_images, draw.CELL_SIZE, 
                'pos only')
        
        if mouse_clicked:
            image_selected.click_image_at_pixel(mouse, interface.list_rect, 
                                                list_of_images, draw.CELL_SIZE)
            
            what_text_is_clicked = event.click_text_at_pixel(
                mouse, interface.text_rects)
            if what_text_is_clicked is not None:
                if what_text_is_clicked == 'new map':
                    cells = event.get_map_size_input()
                    map_.new(cells)
                    # file_read, array = make_map.read()
                    map_began = True
                elif what_text_is_clicked == 'save map':
                    map_.save()
                else:
                    present_layer = what_text_is_clicked
                    print(present_layer)
        
        if mouse_down:
            cell = event.find_cell_at_pixel(mouse, interface.map_rect, cells, 
                                            draw.CELL_SIZE, 'cell')

        if map_began:
            if mouse_down and image_selected:
                if cell is not None and present_layer is not None:
                    map_.draw(cell, present_layer,
                              image_selected.image_selected)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

main()
