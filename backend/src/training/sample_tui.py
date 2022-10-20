
# source: https://docs.python.org/3/howto/curses.html
import curses
from time import sleep

##### CONSTANTS #####
# display
PANEL_HEIGHT = 5
PANEL_WIDTH = 50
Y_PADDING = 3
X_PADDING = 10


def main(stdscr: curses.window):
    # initialize things for TUI
    SCREEN_HEIGHT, SCREEN_WIDTH = stdscr.getmaxyx()
    curses.curs_set(False)  # doesn't display cursor

    # notice that curses uses yx coordinates
    question_window = curses.newwin(
        PANEL_HEIGHT, PANEL_WIDTH, Y_PADDING, X_PADDING)
    answer_window = curses.newwin(
        PANEL_HEIGHT, PANEL_WIDTH, Y_PADDING, 2*X_PADDING+PANEL_WIDTH)

    # write some text
    question_window.addstr("hi")
    question_window.refresh()
    answer_window.addstr("there")
    answer_window.refresh()
    sleep(3)

    # main loop
    while True:
        curses.flushinp()  # flushes input buffer
        c = stdscr.getkey()  # gets next key from input buffer, hangs until there's a key
        stdscr.addstr(20, 15, "sheesh")
        stdscr.refresh()
        question_window.addstr("there\nthere")
        question_window.refresh()
        if c == 'q':
            stdscr.addstr(10, 15, "zzz")
        elif c == 'w':
            stdscr.addstr(10, 15, "yike")
        elif c == 'c':
            stdscr.clear()
        elif c == 'e':
            break


if __name__ == "__main__":
    curses.wrapper(main)
