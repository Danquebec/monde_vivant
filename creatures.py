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

list_of_creatures = []

class Creature:
    '''Anything that moves and can do actions in the game.'''
    def __init__(self, pos, image, speed):
        self.pos = pos
        self.image = image
        self.speed = speed
    def move(self, toward_where):
        if toward_where == 'up':
            self.pos[1] -= 1
        elif toward_where == 'down':
            self.pos[1] += 1
        elif toward_where == 'right':
            self.pos[0] += 1
        elif toward_where == 'left':
            self.pos[0] -= 1


class Human(Creature):
    '''A human.'''
    def __init__(self, pos, image, sex, age, size, strenght, speed):
        self.sex = sex # female or male
        self.age = age
        self.size = size
        # Usually (white ethnicity):
        # Females: 154cm to 174cm. Summum reached at 15 - 20 years old.
        # 4cm smaller at 70 years old.
        # Males: 168cm to 190cm. Summum reached at 20 - 25.
        # 6cm smaller at 15 years old.
        # 4cm smaller at 70 years old.
        # Infants just born: 36cm to 51cm.
        # TODO: create a text in a separate file that would define the game.
        self.strenght = strenght
        # lvl 2 to 7 for male adults. lvl 1 to 6 for female adults. An infant
        # will be 0.
        self.pos = pos
        self.image = image
        self.speed = speed
        # humans take 600 to 100 miliseconds to move throught a cell.
    creature_type = 'organic'


class Peasant(Human):
    '''Peasant males usually have a strenght of 4. Can be 2 to 3 if 
       malnurished. Can be 5 if fat and big.
       Peasant females usually have a strenght of 3. Can be 1 to 2 if 
       malnurished. Can be 4 if fat and big.'''

# Examples (deprecated lol):
'''
garanar = Human((0, 4), 'male', 34, 177, 5, 'garanar')

print(garanar.sex)

peon = Peasant((2, 4), 'male', 44, 170, 3, 'peasant')

print(peon.x)
print(peon.y)

peon.move('UP')

print(peon.x)
print(peon.y)
'''

# Test:
heros = Human([0, 0], 'heros', 'male', 22, 170, 2, 0.300000)
list_of_creatures.append(heros)
