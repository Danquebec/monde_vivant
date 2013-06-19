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

def handling(mouse, mouse_clicked, mouse_down, toward_where):
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
        elif event.type == KEYUP:
            toward_where = False
    return mouse, mouse_clicked, mouse_down, toward_where


def slide_to(slide_to, map_move, CELLSIZE):
    if slide_to:
        if slide_to == 'up':
            map_move[1] -= CELLSIZE
        elif slide_to == 'down':
            map_move[1] += CELLSIZE
        elif slide_to == 'left':
            map_move[0] -= CELLSIZE
        elif slide_to == 'right':
            map_move[0] += CELLSIZE
    return slide_to, map_move


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
