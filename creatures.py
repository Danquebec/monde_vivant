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
from draw import Drawable

list_of_creatures = []


class Creature(object):
    '''Anything that moves and can do actions in the game.'''
    def __init__(self, action, time_length, pos, image, speed, last_hit,
                 final_hit, foe):
        self.action = action
        self.time_length = time_length
        self.pos = pos
        self.image = image
        self.speed = speed
        self.last_hit = last_hit
        self.final_hit = final_hit
        self.foe = foe

    def move(self, blocking_cells_map, toward_where, list_of_creatures):
        def try_to_move(blocking_cells_map, list_of_creatures, x, y):
            def against_obstacle(blocking_cells_map, x, y):
                try:
                    if blocking_cells_map[x][y] == 0:
                        return False
                    elif blocking_cells_map[x][y] == 1:
                        return True
                    else:
                        print('There is a {} in blocking_cells of map! There '
                              'should only be 0 or 1!'.format(blocking_cells_map[x][y]))
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
                    print(blocking_cells_map[x])
         
        if toward_where == 'up':
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


class Humanoid(Creature, Drawable):
    '''A humanoid creature.'''
    def __init__(self, pos=[0,0], action=None, time_length=None, image=None,
                 speed=None, last_hit=None, final_hit=False, foe=None,
                 facing=None, sex=None, age=None, size=None, strength=None,
                 agility=None, strong_hand=None, weak_hand=None):
        Creature.__init__(self, action, time_length, pos, image, speed,
                          last_hit, final_hit, foe)
        #Drawable.__init__(self, image)
        self.sex = sex # female or male
        self.age = age
        self.size = size
        self.strength = strength
        self.facing = facing
        self.gear = {'strong hand':strong_hand,
                     'weak hand':weak_hand}
        self.constitution = 100 + (self.strength * 10)
        self.hit_pts = self.constitution
    type_ = 'intelligent animal'

    def attack_s(self, list_of_creatures):
        self.foe = self.face_other(list_of_creatures)
        if self.foe:
            print('You are attacking {}!'.format(self.foe.image))
            self.last_hit = time()
        else:
            print('There is nothing to attack.')

    def attack_e(self):
        def hit():
            self.foe.get_wound(
                self.gear['strong hand'].base_damage +
                (self.strength * self.gear['strong hand'].damage_scaler))
            if self.final_hit is not True:
                self.last_hit = time()
            else:
                self.last_hit = None
                self.final_hit = None
                self.foe = None
                print('You can’t reach your foe anymore.')

        foe = self.face_other(list_of_creatures)
        if foe is None:
            self.final_hit = True
        self.foe = foe
        hit()

    def face_other(self, list_of_creatures):
        for creature in list_of_creatures:
            if (self.facing == 'up' and self.pos[0] == creature.pos[0] and
                self.pos[1]-1 == creature.pos[1]):
                return creature
            if (self.facing == 'down' and self.pos[0] == creature.pos[0] and
                self.pos[1]+1 == creature.pos[1]):
                return creature
            if (self.facing == 'left' and self.pos[0]-1 == creature.pos[0] and
                self.pos[1] == creature.pos[1]):
                return creature
            if (self.facing == 'right' and self.pos[0]+1 == creature.pos[0] and
                self.pos[1] == creature.pos[1]):
                return creature
        return None

    def get_wound(self, damage):
        self.hit_pts -= damage
        print(self.hit_pts)
    
    def till_s(self):
        error_message = ('You need a hoe to till! Or else you can use '
                        'animals or a machine.')
        try:
            if self.gear['strong hand'].type_ == 'hoe':
                self.action = 'till'
                self.time_length = 1.000000
                print('Started tilling…')
                return time() # TODO: till_animation()

            else:
                print(error_message)
        except AttributeError:
            print(error_message)

    def till_e(self, environment, world):
        environment.add_crop(world, self.pos)
        self.action, self.time_length = None, None
        print('Finished tilling!')


class WieldableObject(object):
    def __init__(self, name, type_, material, base_damage, damage_scaler,
                 minimal_force_1H, minimal_force_2H, speed, chance_reaching,
                 chance_reaching_scaler):
        self.name = name
        self.type_ = type_
        self.material = material
        self.base_damage = base_damage
        self.damage_scaler = damage_scaler
        self.minimal_force_1H = minimal_force_1H
        self.minimal_force_2H = minimal_force_2H
        self.speed = speed
        self.chance_reaching = chance_reaching
        self.chance_reaching_scaler = chance_reaching_scaler

hoe = WieldableObject('iron hoe', 'hoe', 'iron', 41, 1.7, 6, 3, 3.0, 35, 0.6)

# Test:
hero = Humanoid(pos=[1, 1], image='hero', speed=0.300000, facing='down',
                 sex='male', age=22, size=170, strength=20, agility=15,
                 strong_hand=hoe)
peasant = Humanoid(pos=[2, 4], image='hunter-gatherers', speed=0.300000,
                   facing='down', sex='male', age=22, size=170,
                   strength=20, agility=15)
list_of_creatures.append(hero)
list_of_creatures.append(peasant)
