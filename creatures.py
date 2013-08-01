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
                 final_hit, foe, attacker, toward_where, tick, moving):
        self.action = action
        self.time_length = time_length
        self.pos = pos
        self.image = image
        self.speed = speed
        self.last_hit = last_hit
        self.final_hit = final_hit
        self.foe = foe
        self.attacker = attacker
        self.toward_where = toward_where
        self.tick = tick
        self.moving = moving

    def move(self, blocking_cells_map, list_of_creatures):
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
                    if self.image == 'hero':
                        print(self.pos)
         
        if self.toward_where == 'up':
            try_to_move(blocking_cells_map, list_of_creatures,
                        self.pos[0], self.pos[1]-1)
        elif self.toward_where == 'down':
            try_to_move(blocking_cells_map, list_of_creatures,
                        self.pos[0], self.pos[1]+1)
        elif self.toward_where == 'right':
            try_to_move(blocking_cells_map, list_of_creatures,
                        self.pos[0]+1, self.pos[1])
        elif self.toward_where == 'left':
            try_to_move(blocking_cells_map, list_of_creatures,
                        self.pos[0]-1, self.pos[1])

    def first_foot(self, blocking_cells, list_of_creatures):
        if self.action is not None:
            self.action, self.time_length = None, None
            if self.image == 'hero':
                print('You interrupted your action.')
        if self.foe is not None: # if you just went away from your fight
            self.foe.attacker = None
            self.foe = None
            self.last_hit = None
            self.final_hit = False
            if self.image == 'hero':
                print('You interrupted your fight.')
        self.move(blocking_cells, list_of_creatures)
        self.tick = time()
        self.moving = True

    def next_feet(self, blocking_cells, list_of_creatures):
        if time() - self.tick >= self.speed:
            self.move(blocking_cells, list_of_creatures)
            self.tick = time()


class Humanoid(Creature, Drawable):
    '''A humanoid creature.'''
    def __init__(self, pos=[0,0], action=None, time_length=None, image=None,
                 speed=None, last_hit=None, final_hit=False, foe=None,
                 attacker = None, toward_where=None, tick=None, moving=False,
                 facing=None, sex=None, age=None, size=None, strength=None,
                 agility=None, strong_hand=None, weak_hand=None,
                 back_pack=None):
        Creature.__init__(self, action, time_length, pos, image, speed,
                          last_hit, final_hit, foe, attacker, 
                          toward_where, tick, moving)
        #Drawable.__init__(self, image)
        self.sex = sex # female or male
        self.age = age
        self.size = size
        self.strength = strength
        self.facing = facing
        self.gear = {'strong hand':strong_hand,
                     'weak hand':weak_hand,
                     'back pack':back_pack}
        self.constitution = 100 + (self.strength * 10)
        self.hit_pts = self.constitution
    type_ = 'intelligent animal'

    def attack_s(self, list_of_creatures):
        self.foe = self.face_other(list_of_creatures)
        if self.foe:
            print('You are attacking {}!'.format(self.foe.image))
            self.last_hit = time()
            self.foe.attacker = self
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
                self.foe.attacker = None
                self.last_hit = None
                self.final_hit = False
                self.foe = None
                print('You can’t reach your foe anymore.')

        foe = self.face_other(list_of_creatures)
        if foe is None:
            self.final_hit = True
        else:
            self.foe = foe
        hit()

    def equip(self, index_number):
        self.gear['back pack'].put(self.gear['strong hand'], 1)
        self.gear['strong hand'] = self.gear['back pack'].index[index_number]
        if self.image == 'hero':
            print('You have equipped {} in strong hand.'.format(
                    self.gear['back pack'].index[index_number].name))
    '''
    def harvest_e(self, world, environment):
        for crop in environment.crops:
            if self.pos == crop.pos:
                if self.growth_level == 2:
                    try:
                        if self.gear['back pack'].put(wheat, 1) == None:
                            return
                    except ValueError:
    '''

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
        if self.attacker.image == 'hero':
            print('{} looses {} HPs!'.format(self.image, damage))
            print('{} now has {} HPs.'.format(self.image, self.hit_pts))
    
    def plant(self, seeds, day, environment, world):
        try:
            for crop in environment.crops:
                if crop.pos == self.pos:
                    self.gear['back pack'].take(seeds)
                    crop.seed(seeds.name, day, world)
                    print('You planted {}.'.format(seeds.name))
                    return
            print('You have to plant seeds in a crop.')
        except ValueError:
            print('You have no {}.'.format(seeds.name))

    def till_s(self):
        error_message = ('You need a hoe to till! Or else you can use '
                         'animals or a machine.')
        try:
            if self.gear['strong hand'].type_ == 'hoe':
                self.action = 'till'
                self.time_length = 1.000000
                if self.image == 'hero':
                    print('Started tilling…')
                return time() # TODO: till_animation()

            else:
                if self.image == 'hero':
                    print(error_message)
                else:
                    pass
        except AttributeError:
            if self.image == 'hero':
                print(error_message)
            else:
                pass

    def till_e(self, environment, world, day):
        environment.add_crop(world, self.pos, day)
        self.action, self.time_length = None, None
        if self.image == 'hero':
            print('Finished tilling!')

class BasicObject(object):
    def __init__(self, name, type_, space_taken):
        self.name = name
        self.type_= type_
        self.space_taken = space_taken

class WieldableObject(BasicObject):
    def __init__(self, name, type_, material, space_taken, 
                 base_damage, damage_scaler, 
                 minimal_force_1H, minimal_force_2H,
                 speed, chance_reaching, chance_reaching_scaler,
                 state=100):
        BasicObject.__init__(self, name, type_, space_taken)
        self.material = material
        self.space_taken = space_taken
        self.base_damage = base_damage
        self.damage_scaler = damage_scaler
        self.minimal_force_1H = minimal_force_1H
        self.minimal_force_2H = minimal_force_2H
        self.speed = speed
        self.chance_reaching = chance_reaching
        self.chance_reaching_scaler = chance_reaching_scaler
        self.state = state

class InventoryObject(BasicObject):
    def __init__(self, name, type_, space_taken, material, space):
        BasicObject.__init__(self, name, type_, space_taken)
        self.material = material
        self.space = space
        self.content = []
        self.index = {}
    def put(self, introduced_object, number):
        if introduced_object.__class__.__name__ == 'InventoryObject':
            if introduced_object.content != []:
                return ('You can’t put non empty inventory objects in an '
                        'inventory object!')
        inventory_total = 0
        introduced_objects_total = 0
        for thing in self.content:
            inventory_total += thing.space_taken
        for i in xrange(0, number):
            introduced_objects_total += introduced_object.space_taken
        if inventory_total + introduced_objects_total <= self.space:
            for i in xrange(0, number):
                self.content.append(introduced_object)
        else:
            return 'There is not enough space in the inventory object!'
    def take(self, object_taken):
        self.content.remove(object_taken)
    def list_content(self, content_searched):
        index_number = 0
        for thing in self.content:
            if thing.__class__.__name__ == 'WieldableObject':
                print('{}: {}'.format(index_number, thing.name))
                self.index[index_number] = thing
                index_number += 1


hoe = WieldableObject('iron hoe', 'hoe', 'iron', 200, 41, 1.7, 6, 3, 3.0, 35, 
                      0.6)
sickle = WieldableObject('iron sickle', 'sickle', 'iron', 100, 49, 1.2, 1, 0,
                         1.2, 15, 2.5)
leather_back_pack = InventoryObject('leather backpack', 'backpack', 150, 
                                    'leather', 1200)
wheat_seeds = BasicObject('wheat seeds', 'seeds', 10)
wheat = BasicObject('wheat', 'plant', 1200)

hero = Humanoid(pos=[1, 1], image='hero', speed=0.300000, facing='down',
                 sex='male', age=22, size=170, strength=20, agility=15,
                 strong_hand=hoe, back_pack=leather_back_pack)
hero.gear['back pack'].put(wheat_seeds, 10)
hero.gear['back pack'].put(sickle, 1)
peasant = Humanoid(pos=[2, 4], image='peasant', speed=0.300000,
                       facing='down', sex='male', age=22, size=170,
                       strength=20, agility=15)
print(hero.gear['back pack'].content)
list_of_creatures.append(hero)
list_of_creatures.append(peasant)
