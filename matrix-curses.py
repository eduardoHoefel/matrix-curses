#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Matrix-Curses
# See how deep the rabbit hole goes.
# Copyright (c) 2012 Tom Wallroth
#
# Sources on github:
#   http://github.com/devsnd/matrix-curses/
#
# licensed under GNU GPL version 3 (or later)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

from __future__ import unicode_literals
import locale
import time
import curses
import random
from collections import namedtuple
import sys
PYTHON2 = sys.version_info.major < 3
locale.setlocale(locale.LC_ALL, '')
encoding = locale.getpreferredencoding()

########################################################################
# TUNABLES

DROPPING_CHARS = 50
MIN_SPEED = 1
MAX_SPEED = 7
RANDOM_CLEANUP = 100
FPS = 25
SLEEP_MILLIS = 1.0/FPS
USE_COLORS = False
SCREENSAVER_MODE = True
MATRIX_CODE_CHARS = "01"
MATRIX_CODE_CHARS = list(MATRIX_CODE_CHARS)

########################################################################
# CODE

COLOR_CHAR_NORMAL = 1
COLOR_CHAR_HIGHLIGHT = 2
COLOR_WINDOW = 3

NORMAL_ATTR = curses.A_NORMAL
HIGHLIGHT_ATTR = curses.A_REVERSE

CLEAR_STR = ' '

class FallingChar(object):
    
    def __init__(self, WINDOW_HEIGHT, WINDOW_WIDTH, x):
        self.x = x
        self.speed = 1
        self.char = random.choice(MATRIX_CODE_CHARS)
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.reset()
        self.y = randint(0, WINDOW_WIDTH // 3)
        self.max_length = randint(5, self.WINDOW_HEIGHT // 2)
        self.length = 0
    
    def reset(self):
        # self.length = 0
        self.y = 0
        self.speed = randint(1, 3)
    
    def tick(self, scr, steps):
        if self.advances(steps):
            scr.addstr(self.y, self.x, self.char, NORMAL_ATTR)
            self.y += 1
            if self.y >= self.WINDOW_HEIGHT:
               self.reset() 
            self.char = random.choice(MATRIX_CODE_CHARS)
            scr.addstr(self.y, self.x, self.char, HIGHLIGHT_ATTR)
            if self.length < self.max_length:
                self.length += 1
            else:
                clear_y = self.y - self.length
                if clear_y < 0:
                    clear_y += self.WINDOW_HEIGHT
                scr.addstr(clear_y, self.x, CLEAR_STR, NORMAL_ATTR)
            # if window was resized and char is out of bounds, reset
            # self.out_of_bounds_reset(width, height)
            # # make previous char curses.A_NORMAL
            # if USE_COLORS:
                # scr.addstr(self.y, self.x, self.char, curses.color_pair(COLOR_CHAR_NORMAL))
            # else:
                # scr.addstr(self.y, self.x, self.char, curses.A_NORMAL)
                
            # # choose new char and draw it A_REVERSE if not out of bounds
            # self.char = random.choice(FallingChar.matrixchr).encode(encoding)
            # self.y += 1
            # if not self.out_of_bounds_reset(width, height):
                # if USE_COLORS:
                    # scr.addstr(self.y, self.x, self.char, curses.color_pair(COLOR_CHAR_HIGHLIGHT))
                # else:
                    # scr.addstr(self.y, self.x, self.char, curses.A_REVERSE)
    
    def advances(self, steps):
        if steps % (self.speed) == 0:
            return True
        return False
    
    def step(self, steps, scr):
       
        return -1, -1, None

# we don't need a good PRNG, just something that looks a bit random.
def rand():
    # ~ 2 x as fast as random.randint
    a = 9328475634
    while True:
        a ^= (a << 21) & 0xffffffffffffffff;
        a ^= (a >> 35);
        a ^= (a << 4) & 0xffffffffffffffff;
        yield a

r = rand()
def randint(_min, _max):
    if PYTHON2:
        n = r.next()
    else:
        n = r.__next__()
    return (n % (_max - _min)) + _min

def main():
    steps = 0
    scr = curses.initscr()
    scr.nodelay(1)
    curses.curs_set(0)
    curses.noecho()
    
    if USE_COLORS:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(COLOR_CHAR_NORMAL, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(COLOR_CHAR_HIGHLIGHT, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(COLOR_WINDOW, curses.COLOR_GREEN, curses.COLOR_GREEN)
    
    height, width = scr.getmaxyx()    
    lines = []
    for i in range(width):
        if i % 2 == 0:
            l = FallingChar(height, width, i)
            lines.append(l)
        
    scr.refresh()
    while True:
        height, width = scr.getmaxyx()
        for line in lines:
            line.tick(scr, steps)
        # for i in range(RANDOM_CLEANUP):
            # x = randint(0, width-1)
            # y = randint(0, height-1)
            # scr.addstr(y, x, ' ')

        scr.refresh()
        time.sleep(SLEEP_MILLIS)
        if SCREENSAVER_MODE:
            key_pressed = scr.getch() != -1
            if key_pressed:
                raise KeyboardInterrupt()
        steps += 1

try:
    main()
except KeyboardInterrupt:
    curses.endwin()
    curses.curs_set(1)
    curses.reset_shell_mode()
    curses.echo()
