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

import curses_utils
import logo

########################################################################
# TUNABLES

MIN_SPEED = 1
MAX_SPEED = 3
FPS = 25
SLEEP_MILLIS = 1.0/FPS
SCREENSAVER_MODE = False
MATRIX_CODE_CHARS = "01"
MATRIX_CODE_CHARS = list(MATRIX_CODE_CHARS)

########################################################################
# COLORS

COLOR_CHAR_NORMAL = 1
COLOR_CHAR_HIGHLIGHT = 2
COLOR_CHAR_CLEAR = 3

COLOR_GREEN = 46
COLOR_BLACK = 16
COLOR_RED = 196
COLOR_BLUE = 21
COLOR_YELLOW = 226
COLOR_PURPLE = 201
COLOR_CYAN = 51
COLOR_WHITE = 231
COLOR_GRAY_95 = 59


CLEAR_STR = ' '

class FallingChar(object):
    
    def __init__(self, WINDOW_HEIGHT, WINDOW_WIDTH, x):
        self.x = x
        self.char = random.choice(MATRIX_CODE_CHARS)
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.length = 0
        self.max_length = random.randint(4, WINDOW_HEIGHT // 3)
        self.reset()
        self.y = random.randint(4, 8)#4#randint(0, WINDOW_HEIGHT// 2)
        self.last_char = -1
        self.chars_to_clear = []
    
    def reset(self):
        # self.length = 0
        self.y = 0
        self.speed = random.randint(MIN_SPEED, MAX_SPEED)
        self.first_char = True
    
    def tick(self, steps):
        scr = FallingChar.scr
        if self.advances(steps):
            # if len(self.chars_to_clear):
                # self.clear_char(self.chars_to_clear[0])
                # self.chars_to_clear.remove(self.chars_to_clear[0])
            # else:
                if self.first_char:
                    if not logo.logo.is_inside_logo(self.x, self.y):
                        scr.addstr(self.y, self.x, self.char, curses.color_pair(curses_utils.COLOR_CHAR_HIGHLIGHT))
                    self.length += 1
                    self.first_char = False
                    if self.last_char == -1:
                        self.last_char = 0
                else:
                    if not logo.logo.is_inside_logo(self.x, self.y):
                        scr.addstr(self.y, self.x, self.char, curses.color_pair(curses_utils.COLOR_CHAR_NORMAL))
                    self.char = random.choice(MATRIX_CODE_CHARS)
                    self.y += 1
                    if self.y >= self.WINDOW_HEIGHT:
                        self.reset()
                    if not logo.logo.is_inside_logo(self.x, self.y):
                        scr.addstr(self.y, self.x, self.char, curses.color_pair(curses_utils.COLOR_CHAR_HIGHLIGHT))
                    self.length += 1
                if self.length >= self.max_length:
                    self.clear_last_char()

    # def clear_char(self, char_y):
        # scr = FallingChar.scr
        # scr.addstr(char_y, self.x, CLEAR_STR, curses.color_pair(COLOR_CHAR_CLEAR))

    def clear_last_char(self):
        scr = FallingChar.scr
        last_char = self.y - self.max_length
        if last_char < 0:
            last_char = self.WINDOW_HEIGHT + last_char
        curses_utils.set_text(self.x, last_char, CLEAR_STR, curses.color_pair(curses_utils.COLOR_CHAR_CLEAR))
        # if not logo.logo.is_inside_logo(self.x, last_char):
            # scr.addstr(last_char, self.x, CLEAR_STR, curses.color_pair(curses_utils.COLOR_CHAR_CLEAR))
        self.length -= 1
        # self.last_char += 1
        # if self.last_char >= self.WINDOW_HEIGHT:
            # self.last_char = 0
    
    def advances(self, steps):
        if steps % (self.speed) == 0:
            return True
        return False

def main():
    steps = 0
    curses_utils.init()
    scr = curses_utils.get_SCR()
    FallingChar.scr = scr
    
    height, width = scr.getmaxyx()    

    logo.logo.print()
    # for i in range(arch.height):
        # scr.addstr((height - arch.height) // 2 + i, (width - arch.width) // 2, arch.lines[i])

    lines = []
    for i in range(width):
        if i % 2 == 0:
            l = FallingChar(height, width, i)
            lines.append(l)
        
    scr.refresh()
    while True:
        height, width = scr.getmaxyx()
        for line in lines:
            line.tick(steps)
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
