
import curses_utils
import curses


class Logo(object):

    def __init__(self):
        self.lines = [
                "                   -`                  ",
                "                  .o+`                 ",
                "                 `ooo/                 ",
                "                `+oooo:                ",
                "               `+oooooo:               ",
                "               -+oooooo+:              ",
                "             `/:-:++oooo+:             ",
                "            `/++++/+++++++:            ",
                "           `/++++++++++++++:           ",
                "          `/+++ooooooooooooo/`         ",
                "         ./ooosssso++osssssso+`        ",
                "        .oossssso-````/ossssss+`       ",
                "       -osssssso.      :ssssssso.      ",
                "      :osssssss/        osssso+++.     ",
                "     /ossssssss/        +ssssooo/-     ",
                "   `/ossssso+/:-        -:/+osssso+-   ",
                "  `+sso+:-`                 `.-/+oso:  ",
                " `++:.                           `-/+/ ",
                " .`                                 `/ ",
                ]

        self.lines = [list(line) for line in self.lines]
        
        self.width = len(self.lines[0])
        self.height = len(self.lines)

        self.bolds = set()
        for i in range(9):
            self.bolds.add((i, '?'))

        self.bolds.add((7, 16))
        self.bolds.add((7, 17))



    def print(self):
        scr = curses_utils.get_SCR()
        height, width = curses_utils.get_size()
        for i in range(self.height):
            for j in range(self.width):
                style = curses.color_pair(curses_utils.COLOR_CHAR_LOGO_1)
                if (i, '?') in self.bolds or (i, j) in self.bolds:
                    style = curses.color_pair(curses_utils.COLOR_CHAR_LOGO_2) + curses.A_BOLD
                scr.addstr((height - self.height) // 2 + i, (width - self.width) // 2 + j, self.lines[i][j], style)

    def is_inside_logo(self, x, y):
        logo_start_y, logo_start_x = self.get_logo_start()
        logo_end_y, logo_end_x = self.get_logo_end()
        return x >= logo_start_x and x < logo_end_x and y >= logo_start_y and y < logo_end_y and self.get_char_at(x, y) != ' '

    def get_char_at(self, x, y):
        logo_start_y, logo_start_x = self.get_logo_start()
        y -= logo_start_y
        x -= logo_start_x
        return self.lines[y][x]
        

    def get_logo_start(self):
        height, width = curses_utils.get_size()
        return (height - self.height) // 2, (width - self.width) // 2

    def get_logo_end(self):
        height, width = curses_utils.get_size()
        return (height + self.height) // 2, (width + self.width) // 2

logo = Logo()

        

