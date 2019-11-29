import curses
from time import sleep
import psutil
from psutil._common import bytes2human


def cpu(pad):
    use = psutil.cpu_percent()
    bar_length = int((use / 100) * 20)
    pad.addstr(4, 13, str(use) + '%')
    pad.addch(4, 41, '|')
    for i in range(20):
        if i <= bar_length:

            pad.addch(4, 21 + i, ' ', curses.A_STANDOUT)
        else:
            pad.addch(4, 21 + i, ' ')
    curr = 8
    core = 1
    cores = psutil.cpu_percent(percpu=True)
    pad.addstr(6, 3, 'Number of logical CPU: ' + str(len(cores)))
    for per in cores:
        use = per
        bar_length = int((int(use) / 100) * 20)
        pad.addstr(curr, 3, 'Core ' + str(core))
        pad.addstr(curr, 13, str(use) + '%')
        pad.addch(4, 41, '|')
        for i in range(20):
            if i <= bar_length:

                pad.addch(curr, 21 + i, ' ', curses.A_STANDOUT)
            else:
                pad.addch(curr, 21 + i, ' ')
        pad.addch(curr, 41, '|')
        core += 1
        curr += 2
    pad.addstr(curr, 3, 'CPU Frequency: ' + str(psutil.cpu_freq()[0]))
    curr += 2
    pad.addstr(curr, 3, 'Number of processes: '+str(len(psutil.pids())))


def main_mem(pad):


def main(stdscr):
    curses.curs_set(0)
    pad = stdscr
    pad.nodelay(True)
    pad.addstr(1, 2, 'RESOURCE MONITOR', curses.A_BOLD)
    pad.addstr(3, 2, 'CPU STATS')
    pad.addstr(4, 3, 'CPU USAGE')

    pad.refresh()
    while True:
        cpu(pad)
        pad.refresh()
        sleep(0.1)
        if pad.getch() > 0:
            exit()


curses.wrapper(main)
