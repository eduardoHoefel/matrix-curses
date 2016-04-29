def get(LOGO):
    import curses_utils

    bolds = set()

    ## ARCH LOGO

    lines = [
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
            " .`                                 `/ "]


    for i in range(9):
        bolds.add((i, '?'))
    for i in range(6):
        bolds.add((9, 10 + i))
        bolds.add((9, 24 + i))
    for i in range(2):
        bolds.add((10, 9 + i))
        bolds.add((10, 29 + i))

    return lines, bolds, curses_utils.COLOR_BLUE, curses_utils.COLOR_CYAN
