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
    
    def __init__(self, WINDOW_HEIGHT, WINDOW_WIDTH, x, STATE):
        self.STATE = STATE
        self.x = x
        self.char = random.choice(MATRIX_CODE_CHARS)
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.length = 0
        self.max_length = random.randint(4, WINDOW_HEIGHT // 3)
        self.reset()
        self.y = random.randint(2, 8)#4#randint(0, WINDOW_HEIGHT// 2)
        self.last_char = -1
        self.chars_to_clear = []
        if self.STATE == 1:
            self.y = 0
            self.max_length = WINDOW_HEIGHT // 3
            self.speed = MAX_SPEED

    
    def reset(self):
        self.y = 0
        self.speed = random.randint(MIN_SPEED, MAX_SPEED)
        self.first_char = True
    
    def tick(self, steps):
        if self.STATE == 2:
            self.clear_last_char()
            return

        scr = FallingChar.scr
        if self.advances(steps):
            if self.first_char:
                if self.STATE == 1 or not logo.logo.is_inside_logo(self.x, self.y):
                    scr.addstr(self.y, self.x, self.char, curses.color_pair(curses_utils.COLOR_CHAR_HIGHLIGHT))

                self.length += 1
                self.first_char = False
                if self.last_char == -1:
                    self.last_char = 0

            else:
                if self.STATE == 1 or not logo.logo.is_inside_logo(self.x, self.y):
                    scr.addstr(self.y, self.x, self.char, curses.color_pair(curses_utils.COLOR_CHAR_NORMAL))

                self.char = random.choice(MATRIX_CODE_CHARS)
                self.y += 1
                if self.y >= self.WINDOW_HEIGHT:
                    if self.STATE >= 1:
                        #set_gambiarra(True)
                        self.length += 1
                        self.clear_last_char()
                        #set_gambiarra(False)
                        self.STATE = 2
                        return

                    else:
                        self.reset()

                if self.STATE == 1 or not logo.logo.is_inside_logo(self.x, self.y):
                    scr.addstr(self.y, self.x, self.char, curses.color_pair(curses_utils.COLOR_CHAR_HIGHLIGHT))

                self.length += 1
            if self.length >= self.max_length:
                self.clear_last_char()


    def clear_last_char(self):
        if self.length <= 0:
            return

        scr = FallingChar.scr
        last_char = self.y - self.length
        if last_char < 0:
            last_char = self.WINDOW_HEIGHT + last_char

        if self.STATE >= 1 or not logo.logo.is_inside_logo(self.x, last_char):
            scr.addstr(last_char, self.x, CLEAR_STR, curses.color_pair(curses_utils.COLOR_CHAR_CLEAR))
        self.length -= 1
    
    def advances(self, steps):
        if steps % (self.speed) == 0:
            return True
        return False


PASSWORD = []

def main():
    import subprocess
    from subprocess import Popen
    STATE = 0
    steps = 0
    curses_utils.init()
    scr = curses_utils.get_SCR()
    FallingChar.scr = scr
    
    height, width = scr.getmaxyx()    
    width = width - 1

    logo.logo.print()

    lines = []
    for i in range(width):
        if i % 2 == 0:
            l = FallingChar(height, width, i, STATE)
            lines.append(l)
        
    scr.refresh()
    while True:
        for line in lines:
            line.tick(steps)
            if line.STATE == 2 and STATE == 1:
                STATE = 2

        scr.refresh()
        time.sleep(SLEEP_MILLIS)
        if STATE == 2:
            STATE = 3
            for i in range(width):
                l = FallingChar(height, width, i, 1)
                lines.append(l)
            # for i in range(width):
                # if i % 2 == 0:
                    # l = FallingChar(height, width, i, 1)
                    # lines.append(l)

       
        if STATE == 0:
            try:
                key = scr.getkey() 
                if key:
                    if key == '\n':
                        PASSWORD_STRING = ''.join(PASSWORD)
                        del PASSWORD[:]
                        import os
                        FNULL = open(os.devnull, 'w')
                        p1 = subprocess.Popen(["echo", PASSWORD_STRING], stdout=subprocess.PIPE)
                        p2 = subprocess.Popen(["/usr/bin/sudo", "-S", "-k", "true"], stdin=p1.stdout, stdout=FNULL, stderr=FNULL)

                        data = p2.communicate()[0]
                        exit_status = p2.returncode

                        if exit_status == 0:
                            p1 = subprocess.Popen(["/usr/bin/fish", "-c", "unlock"])

                            STATE = 1
                            for line in lines:
                                line.STATE = 1

                        else:
                            pass


                        # return p2.communicate()[0]
                        # return None
                    else:
                        PASSWORD.append(key)
            except Exception:
                pass

        steps += 1

try:
    ret = main()
    curses.endwin()
    curses.curs_set(1)
    curses.reset_shell_mode()
    curses.echo()
    
    print(ret)

except KeyboardInterrupt:
    curses.endwin()
    curses.curs_set(1)
    curses.reset_shell_mode()
    curses.echo()
