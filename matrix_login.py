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
from collections import namedtuple
import locale
import time
import curses
import random
import sys
PYTHON2 = sys.version_info.major < 3
locale.setlocale(locale.LC_ALL, '')
encoding = locale.getpreferredencoding()

import curses_utils
from logo import logo

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
        self.y = random.randint(-8, 0)#4#randint(0, WINDOW_HEIGHT// 2)
        self.last_char = -1
        self.chars_to_clear = []
        if self.STATE != 0:
            self.max_length = WINDOW_HEIGHT // 3
            self.speed = MIN_SPEED

    
    def reset(self):
        self.y = 0
        if self.STATE == 0:
            self.speed = random.randint(MIN_SPEED, MAX_SPEED)
        self.first_char = True
    
    def tick(self, steps):
        if self.is_dead():
            self.clear_last_char()
            return

        scr = FallingChar.scr
        if self.advances(steps):
            if self.y < 0:
                self.y += 1;
                return
            if self.first_char:
                if self.is_abount_to_die() or not logo.is_inside_logo(self.x, self.y):
                    scr.addstr(self.y, self.x, self.char, curses.color_pair(curses_utils.COLOR_CHAR_HIGHLIGHT))

                self.length += 1
                self.first_char = False
                if self.last_char == -1:
                    self.last_char = 0

            else:
                if self.is_abount_to_die() or not logo.is_inside_logo(self.x, self.y):
                    scr.addstr(self.y, self.x, self.char, curses.color_pair(curses_utils.COLOR_CHAR_NORMAL))

                self.char = random.choice(MATRIX_CODE_CHARS)
                self.y += 1
                if self.y >= self.WINDOW_HEIGHT:
                    if self.STATE >= 1:
                        #set_gambiarra(True)
                        self.length += 1
                        self.clear_last_char()
                        #set_gambiarra(False)
                        self.STATE += 1
                        if self.STATE == 3:
                            return

                        self.x -= 1

                    self.reset()

                if self.is_abount_to_die() or not logo.is_inside_logo(self.x, self.y):
                    scr.addstr(self.y, self.x, self.char, curses.color_pair(curses_utils.COLOR_CHAR_HIGHLIGHT))

                self.length += 1
            if self.length >= self.max_length:
                self.clear_last_char()

    def is_healthy(self):
        return self.STATE == 0

    def is_abount_to_die(self):
        return self.STATE == 1 or self.STATE == 2

    def is_dead(self):
        return self.STATE == 3

    def clear_last_char(self):
        if self.length <= 0 or self.y < 0:
            return

        x_to_clear = self.x
        scr = FallingChar.scr
        last_char = self.y - self.length
        if last_char < 0:
            last_char = self.WINDOW_HEIGHT + last_char
            if self.STATE == 2:
                x_to_clear += 1

        if self.STATE >= 1 or not logo.is_inside_logo(self.x, last_char):
            scr.addstr(last_char, x_to_clear, CLEAR_STR, curses.color_pair(curses_utils.COLOR_CHAR_CLEAR))
        self.length -= 1
    
    def advances(self, steps):
        return steps % (self.speed) == 0

S_NORMAL = 0
S_LOGIN_SUCCESS = 1
S_FINISHED = 2

def main():
    import subprocess
    STATE = 0
    steps = 0
    curses_utils.init()
    scr = curses_utils.get_SCR()
    FallingChar.scr = scr
    
    height, width = scr.getmaxyx()    
    width -= 1

    logo.print()

    lines = []
    for i in range(width):
        if i % 2 == 0:
            l = FallingChar(height, width, i, 0)
            lines.append(l)
        
    scr.refresh()
    del_lines = []
    while True:
        scr.refresh()
        if STATE == S_LOGIN_SUCCESS:
            STATE = S_FINISHED

        for line in lines:
            line.tick(steps)
            if STATE == S_FINISHED and (line.STATE != 3 or line.length > 0):
                STATE = S_LOGIN_SUCCESS

        if STATE == S_FINISHED:
            return
        time.sleep(SLEEP_MILLIS)
        if STATE == 2:
            STATE = 3
       
        if STATE == 0:
            try:
                key = scr.getkey() 
                if key:
                    if key == '\x7f' or key == '\x15':
                        logo.password_erase()

                    elif key == '\n':
                        import os

                        PASSWORD_STRING = ''.join(logo.PASSWORD)
                        logo.password_delete()
                        FNULL = open(os.devnull, 'w')
                        p1 = subprocess.Popen(["echo", PASSWORD_STRING], stdout=subprocess.PIPE)
                        p2 = subprocess.Popen(["/usr/bin/sudo", "-S", "-k", "true"], stdin=p1.stdout, stdout=FNULL, stderr=FNULL)

                        data = p2.communicate()[0]
                        exit_status = p2.returncode

                        if exit_status == 0:
                            p1 = subprocess.Popen(["/usr/bin/fish", "-c", "unlock"])

                            STATE = 1
                            new_lines = []
                            logo_start_y, logo_start_x = logo.get_logo_start()
                            dummy, logo_end_x = logo.get_logo_end()
                            for line in lines:
                                line.STATE = 1
                                line.speed = 1
                                if line.y >= logo_start_y and line.x >= logo_start_x and line.x < logo_end_x:
                                    new_line = FallingChar(height, width, line.x, 2)
                                    new_line.speed = 1
                                    new_line.y = int(new_line.y * random.uniform(1, 7))
                                    new_lines.append(new_line)
                            for line in new_lines:
                                lines.append(line)

                            lines[0].STATE = 2

                        else:
                            pass

                    else:
                        value = ord(key)
                        if value > 32 and value != 127:
                            logo.password_append(key)
            except Exception:
                pass

        steps += 1

import os
if not os.path.exists(os.path.expanduser("~") + "/.config/login/LOGED"):
    try:
        main()

    except KeyboardInterrupt:
        pass

    curses.endwin()
    curses.curs_set(1)
    curses.reset_shell_mode()
    curses.echo()
    # for char in logo.PASSWORD:
        # print(ord(char))
    # print(logo.PASSWORD)
