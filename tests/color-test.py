import curses

def test_colors(stdscr):
    curses.start_color()
    curses.use_default_colors()

    # Initialize colors
    for i in range(16):
        curses.init_pair(i + 1, i, -1)

    color_names = [
        "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
        "light_grey", "dark_grey", "light_red", "light_green", "light_yellow",
        "light_blue", "light_magenta", "light_cyan"
    ]

    stdscr.clear()
    
    for i, color in enumerate(color_names):
        stdscr.addstr(i, 0, f"{color}", curses.color_pair(i + 1))
    
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(test_colors)