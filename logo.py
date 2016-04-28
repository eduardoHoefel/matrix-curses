
import curses_utils
import curses


class Logo(object):

    def __init__(self):

        self.PASSWORD = []

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
                "                                       ",
                "                                       ",
                "          Username:                    ",
                "          Password:                    ",
                "                                       "]

        self.lines = [list(line) for line in self.lines]
        
        self.width = len(self.lines[0])
        self.height = len(self.lines)

        self.bolds = set()
        for i in range(9):
            self.bolds.add((i, '?'))
        for i in range(6):
            self.bolds.add((9, 10 + i))
            self.bolds.add((9, 24 + i))
        for i in range(2):
            self.bolds.add((10, 9 + i))
            self.bolds.add((10, 29 + i))

        self.U_pos = (21, 10)
        for i in range(self.U_pos[0], self.U_pos[0] + 2):
            for j in range(self.U_pos[1], 20):
                self.bolds.add((i, j))
        
        # import subprocess
        # process = subprocess.Popen(["echo", "$USER"])
        # name = process.communicate()[0]
        import getpass
        name = getpass.getuser()
        N_pos = (self.U_pos[0], self.U_pos[1] + len("Username: "))
        for i in list(name):
            self.lines[N_pos[0]][N_pos[1]] = i
            N_pos = (N_pos[0], N_pos[1] + 1)






    def print(self):
        scr = curses_utils.get_SCR()
        height, width = curses_utils.get_size()
        for i in range(self.height):
            for j in range(self.width):
                if self.lines[i][j] == '#':
                    continue;
                style = curses.color_pair(curses_utils.COLOR_CHAR_LOGO_1)
                if (i, '?') in self.bolds or (i, j) in self.bolds:
                    style = curses.color_pair(curses_utils.COLOR_CHAR_LOGO_2) + curses.A_BOLD
                scr.addstr((height - self.height) // 2 + i, (width - self.width) // 2 + j, self.lines[i][j], style)

    def is_inside_logo(self, x, y):
        logo_start_y, logo_start_x = self.get_logo_start()
        logo_end_y, logo_end_x = self.get_logo_end()
        return x >= logo_start_x and x < logo_end_x and y >= logo_start_y and y < logo_end_y and self.is_solid(x, y)

    def is_solid(self, x, y):
        password_start = self.get_password_start()
        if y == password_start[0]:
            if x >= password_start[1] and x <= password_start[1] + len(self.PASSWORD):
                return True

        char = self.get_char_at(x, y)
        return char != ' ' and char != '#'

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

    def get_password_start(self):
        logo_start = self.get_logo_start()
        password_start = (logo_start[0] + self.U_pos[0] + 1, logo_start[1] + self.U_pos[1] + len("Password:"))
        return password_start

    def clear_password(self):
        del self.PASSWORD[:]

    def password_append(self, char):
        self.PASSWORD.append(char)
        scr = curses_utils.get_SCR()
        password_start = self.get_password_start()
        scr.addstr(password_start[0], password_start[1] + len(self.PASSWORD), '*', curses.color_pair(curses_utils.COLOR_CHAR_LOGO_1))
    
    def password_erase(self):
        scr = curses_utils.get_SCR()
        password_start = self.get_password_start()
        scr.addstr(password_start[0], password_start[1] + len(self.PASSWORD), ' ', curses.color_pair(curses_utils.COLOR_CHAR_LOGO_1))
        self.PASSWORD.pop()

    def password_delete(self):
        password_start = self.get_password_start()
        while len(self.PASSWORD):
            self.password_erase()



logo = Logo()

        

