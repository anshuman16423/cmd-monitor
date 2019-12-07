import curses
from time import sleep
import psutil


def main(stdscr):
    curses.curs_set(0)
    stdscr.scrollok(True)
    stdscr.idlok(True)
    pad = stdscr
    pad.nodelay(True)
    pad.addstr(1, 2, 'CPU USAGE GRAPH', curses.A_DIM)

    dq = [0] * 80  # deque of length 20 i,e. stores previous 20 values
    # initials 4 and 30
    while True:
        per = psutil.cpu_percent()
        pad.addstr(2, 2, 'Current Usage: ' + str(per) + '%')
        dq.append(int((int(per) * 20) / 100))
        # print(dq)
        dq.pop(0)
        prev = dq[0]
        for row in range(4, 84):
            # print(prev,dq[row-4])
            for col in range(21):
                if dq[row - 4] <= prev:
                    if prev >= col >= dq[row - 4]:
                        pad.addch(30 - col, row, "-")
                    else:
                        pad.addch(30 - col, row, ' ')
                else:
                    if prev <= col <= dq[row - 4]:
                        pad.addch(30 - col, row, '-')
                    else:
                        pad.addch(30 - col, row, ' ')
            prev = dq[row - 4]
        pad.refresh()
        sleep(1)
        if pad.getch() > 0:
            exit()





curses.wrapper(main)