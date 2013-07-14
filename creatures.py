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

from time import time

list_of_creatures = []

class Creature:
    '''Anything that moves and can do actions in the game.'''
    def __init__(self, pos, image, speed, ):
        self.pos = pos
        self.image = image
        self.speed = speed
        
    def move(self, blocking_cells_map, toward_where, list_of_creatures):
        def try_to_move(blocking_cells_map, list_of_creatures, x, y):
            def against_obstacle(blocking_cells_map, x, y):
                try:
                    if blocking_cells_map[x][y] == 0:
                        print(blocking_cells_map[x])
                        return False
                    elif blocking_cells_map[x][y] == 1:
                        return True
                    else:
                        print('There is a {} in blocking_cells of map! There '
                              'should only be 1 or 2!'.format(blocking_cells_map[x][y]))
                        raise
                except IndexError:
                    print(blocking_cells_map[0][0])
                    return True

            def against_creature(list_of_creatures, x, y):
                for creature in list_of_creatures[1:]:
                    if creature.pos[0] == x and creature.pos[1] == y:
                        return True
                    else:
                        return False

            if x >= 0 and y >= 0:
                if (not against_obstacle(blocking_cells_map, x, y) and not
                        against_creature(list_of_creatures, x, y)):
                    self.pos = [x, y]
         
        if toward_where == 'up':
            '''
            if (try_obstacle(
                    blocking_cells_map, self.pos[0], self.pos[1]-1) and
                    try_creature(
                    list_of_creatures, self.pos[0], self.pos[1]-1)):
                self.pos[1] =- 1
            # try_to_move(blocking_cells_map, self.pos[0], self.pos[1]-1)
            '''
            try_to_move(blocking_cells_map, list_of_creatures,
                        self.pos[0], self.pos[1]-1)
        elif toward_where == 'down':
            try_to_move(blocking_cells_map, list_of_creatures,
                        self.pos[0], self.pos[1]+1)
        elif toward_where == 'right':
            try_to_move(blocking_cells_map, list_of_creatures,
                        self.pos[0]+1, self.pos[1])
        elif toward_where == 'left':
            try_to_move(blocking_cells_map, list_of_creatures,
                        self.pos[0]-1, self.pos[1])


class Humanoid(Creature):
    '''A humanoid creature.'''
    def __init__(self, pos, image, sex, age, size, strenght, speed,
                 strong_hand_wield=None, weak_hand_wield=None):
        self.sex = sex # female or male
        self.age = age
        self.size = size
        self.strenght = strenght
        self.pos = pos
        self.image = image
        self.speed = speed
        # humans take 600 to 100 miliseconds to move throught a cell.
        self.equipment = {'strong hand wield':strong_hand_wield,
                          'weak hand wield':weak_hand_wield}
    type_ = 'intelligent animal'
    
    def till(self, environment, world):
        error_message = ('You need a hoe to till! Or else you can use '
                        'animals or a machine.')
        try:
            if self.equipment['strong hand wield'].type_ == 'hoe':
                start = time()
                print('Started tilling…')
                while time() < start + 1.000000:
                    pass
                    # TODO: till_animation()
                print('wut')
                environment.add_crop(world, self.pos)
                print('Finished tilling!')
            else:
                print(error_message)
                print(self.equipment['strong hand wield'].type_)
        except AttributeError:
            print(error_message)
            print(self.equipment)
            print(self.equipment['strong hand wield'].type_)


class WieldableObject:
    def __init__(self, name, type_, material):
        self.name = name
        self.type_ = type_
        self.material = material

hoe = WieldableObject('iron hoe', 'hoe', 'iron')

# Test:
heros = Humanoid([1, 1], 'heros', 'male', 22, 170, 20, 0.300000, 
strong_hand_wield=hoe)
peasant = Humanoid([2, 4], 'hunter-gatherers', 'male', 22, 170, 20, 0.300000)
list_of_creatures.append(heros)
list_of_creatures.append(peasant)
