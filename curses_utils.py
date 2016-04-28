

import curses


COLOR_GREEN = 46
COLOR_BLACK = 16
COLOR_RED = 196
COLOR_BLUE = 21
COLOR_YELLOW = 226
COLOR_PURPLE = 201
COLOR_CYAN = 51
COLOR_WHITE = 231
COLOR_GRAY_95 = 59


COLOR_CHAR_NORMAL = 1
COLOR_CHAR_HIGHLIGHT = 2
COLOR_CHAR_CLEAR = 3
COLOR_CHAR_LOGO_1 = 4
COLOR_CHAR_LOGO_2 = 5

class MyClass:

    def __init__(self):
        pass

    def init(self):
        scr = curses.initscr()
        self.SCR = scr

        scr.nodelay(1)
        curses.curs_set(0)
        curses.noecho()
        curses.raw()

        curses.start_color()
        curses.use_default_colors()

        curses.init_pair(COLOR_CHAR_NORMAL, COLOR_GREEN, COLOR_BLACK)
        curses.init_pair(COLOR_CHAR_HIGHLIGHT, COLOR_BLACK, COLOR_GREEN)
        curses.init_pair(COLOR_CHAR_CLEAR, COLOR_GRAY_95, COLOR_BLACK)
        curses.init_pair(COLOR_CHAR_LOGO_1, COLOR_BLUE, COLOR_BLACK)
        curses.init_pair(COLOR_CHAR_LOGO_2, COLOR_CYAN, COLOR_BLACK)


myObject = MyClass()


def init():
    myObject.init()
    
def get_SCR():
    return myObject.SCR

def get_size():
    return get_SCR().getmaxyx()

import logo

def set_text(x, y, char, style):
    if not logo.logo.is_inside_logo(x, y):
        get_SCR().addstr(y, x, char, style)


