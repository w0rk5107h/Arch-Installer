import curses
from curses import wrapper
import helperText

def main(stdscr):

    # FETCH THE SCREEN COORDINATES
    MAX_Y = curses.LINES
    MAX_X = curses.COLS

    stdscr.clear()
    stdscr.addstr((MAX_Y-11)//2,(MAX_X-11)//2, helperText.welcomeMessage)
    stdscr.refresh()
    stdscr.getch()

wrapper(main)