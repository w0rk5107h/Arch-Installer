import curses
from curses import wrapper
import helperText
from subprocess import check_output
from os import system

TASKS = ['welcome', 'setKeyMap']
TASK = 0

def quit(stdscr):
    exit()

# welcome screen
def welcome(stdscr):
    global TASK
    global TASKS
    
    stdscr.clear()
    stdscr.addstr(helperText.welcomeMessage)
    stdscr.refresh()
    while True:
        key = stdscr.getkey()
        if key == curses.KEY_ENTER:
            TASK += 1
            break
        elif key.lower() == 'q':
            quit()
            break

# key map settings
def setKeyMap(stdscr):
    global TASK
    global TASKS

    keyMap = check_output("localectl status | awk -F ':' '{print $2}' | head -n 1").decode().strip()
    stdscr.clear()
    stdscr.addstr(helperText.setKeyMapMessage.replace('##keyMap##', keyMap))
    stdscr.refresh()
    while True:
        key = stdscr.getkey()
        if key == curses.KEY_ENTER:
            TASK += 1
            break
        elif key.lower() == 'c':
            keyMaps = check_output('localectl list-keymaps', shell=True).decode().strip().split('\n')
            f = open('keyMapFile','w+')
            f.write(helperText.keyMapFileMessage)
            count = 1
            for keyMap in keyMaps:
                f.write(f'{count}  -->  {keyMap}\n')
                count += 1
            f.close()
            while key.lower() == 'c':
                system('less keyMapFile')
                stdscr.clear()
                stdscr.addstr(helperText.enterYourKeyMapMessage)
                stdscr.refresh()
                index = ''
                while True:
                    key = stdscr.getkey()
                    if key.lower() == 'c':
                        break
                    elif key == curses.KEY_ENTER:
                        if index.isdigit():
                            index = int(index)
                            if index >= 1 and index <= len(keyMaps)+1:
                                pass
                            else:
                                key = 'c'
                            break
                        else:
                            key = 'c'
                            break
                    elif key.isdigit():
                        index += key
                        stdscr.addstr(key)
                        stdscr.refresh()
            system(f'loadkeys {keyMaps[index-1]}')
            TASK += 1
            break
        elif key.lower() == 'KEY_BACKSPACE':
            TASK -= 1
            break

def main(stdscr):
    global TASK
    global TASKS

    
    while True:
        if TASKS[TASK] == 'welcome':
            welcome(stdscr)
        elif TASKS[TASK] == 'setKeyMap':
            setKeyMap(stdscr)
        elif TASK > len(TASKS):
            break
    stdscr.getch()

wrapper(main)