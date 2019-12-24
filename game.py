import curses
from time import sleep


def main(stdscr):
    jump = []
    curses.curs_set(0)
    stdscr.scrollok(True)
    stdscr.idlok(True)
    pad = stdscr
    pad.nodelay(True)
    score = 0
    block = [0] * 60
    for i in range(60):
        if (i+5) % 20 == 0:
            block[i] = 1
    c=0
    base=[0]*59
    for i in range(59):
        if i%2:
            base[i]=' '
        else:
            base[i]='-'
    while True:
        for i in range(59):
            pad.addch(10,5+i,base[i])
        base.append(base.pop(0))
        pad.addstr(2,45,'Score: '+str(score))
        score += 5
        if pad.getch() == 97 and not jump:
            jump = [8, 7, 7.5, 6, 6.5, 5, 4, 5, 6.5, 6,  7, 7.5, 8]
        try:
            ht = jump.pop(0)
        except:
            ht = 9
        if block[0] and ht>=8:
            print("Score: "+str(score))
            exit()
        for i in range(2, 10):
            if i == ht:

                pad.addstr(ht, 6, ' ', curses.A_STANDOUT)
            else:
                pad.addstr(i, 6, ' ')
        for i in range(60):
            if block[i]:
                pad.addch(8, 6+i, ' ', curses.A_STANDOUT)
                pad.addch(9, 6+i, ' ', curses.A_STANDOUT)
            elif i or ht < 9:
                pad.addch(8, 6 + i, ' ')
                pad.addch(9, 6 + i, ' ')
            elif ht < 10:
                pad.addch(8, 6 + i, ' ')
        block.append(block.pop(0))
        sleep(0.04)


curses.wrapper(main)
