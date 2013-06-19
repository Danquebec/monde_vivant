#!/usr/bin/python
# -*- coding:utf-8 -*-

# Societes2 © 2012 Daniel Dumaresq
# e-mail: danquebec@singularity.fr
# Jabber: danquebec@louiz.org

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

# TODO: Do something about this… lol.

from random import randint

def get_random_color():
    return [randint(0, 255) for time in range(3)]
