import curses
from time import sleep
import psutil
from psutil._common import bytes2human
import time
from threading import Thread
import os

EXIT = False


def cpu(pad):
    use = psutil.cpu_percent()
    bar_length = int((use / 100) * 20)
    pad.addstr(4, 13, str(use) + '% ')
    pad.addch(4, 41, '|')
    for i in range(20):
        if i <= bar_length:

            pad.addch(4, 21 + i, ' ', curses.A_STANDOUT)
        else:
            pad.addch(3, 21 + i, ' ', curses.A_UNDERLINE)

            pad.addch(4, 21 + i, ' ', curses.A_UNDERLINE)
    curr = 8
    core = 1
    cores = psutil.cpu_percent(percpu=True)
    pad.addstr(6, 3, 'Number of logical CPU: ' + str(len(cores)))
    for per in cores:
        use = per
        bar_length = int((int(use) / 100) * 20)
        pad.addstr(curr, 3, 'Core ' + str(core))
        pad.addstr(curr, 13, str(use) + '% ')
        pad.addch(4, 41, '|')
        for i in range(20):
            if i <= bar_length:

                pad.addch(curr, 21 + i, ' ', curses.A_STANDOUT)
            else:
                pad.addch(curr - 1, 21 + i, ' ', curses.A_UNDERLINE)
                pad.addch(curr, 21 + i, ' ', curses.A_UNDERLINE)
        pad.addch(curr, 41, '|')
        core += 1
        curr += 2
    try:

        pad.addstr(curr, 3, 'CPU Frequency: ' + str(psutil.cpu_freq()[0]))
        curr += 2
    except:
        pad.addstr(curr, 3, 'CPU Frequency: Not found')
        curr += 2
    pad.addstr(curr, 3, 'Number of processes: ' + str(len(psutil.pids())))

    curr += 4
    pad.addstr(curr - 2, 2, '-' * 41)
    return curr


def main_mem(pad, start):
    pad.scrollok(1)
    curr = start
    pad.addstr(curr, 2, 'MAIN MEMORY')
    curr += 2
    mem = psutil.virtual_memory()
    pad.addstr(curr, 3, 'Used: ' + str(mem.percent) + '%')
    bar_length = int((int(mem.percent) / 100) * 20)
    for i in range(20):
        if i <= bar_length:
            pad.addch(curr, 21 + i, ' ', curses.A_STANDOUT)
        else:
            pad.addch(curr - 1, 21 + i, ' ', curses.A_UNDERLINE)
            pad.addch(curr, 21 + i, ' ', curses.A_UNDERLINE)
    pad.addch(curr, 41, '|')
    curr += 2
    pad.addstr(curr, 3, 'Total: ' + bytes2human(mem.total))
    curr += 2
    pad.addstr(curr, 3, 'Used: ' + bytes2human(mem.used))
    curr += 2
    pad.addstr(curr, 2, 'SWAP MEMORY')
    curr += 2
    mem = psutil.swap_memory()
    pad.addstr(curr, 3, 'Used: ' + str(mem.percent) + '%')
    bar_length = int((int(mem.percent) / 100) * 20)
    for i in range(20):
        if i <= bar_length:

            pad.addch(curr, 21 + i, ' ', curses.A_STANDOUT)
        else:
            pad.addch(curr - 1, 21 + i, ' ', curses.A_UNDERLINE)
            pad.addch(curr, 21 + i, ' ', curses.A_UNDERLINE)
    pad.addch(curr, 41, '|')
    curr += 2
    pad.addstr(curr, 3, 'Total: ' + bytes2human(mem.total))
    curr += 2
    pad.addstr(curr, 3, 'Used: ' + bytes2human(mem.used))
    curr += 2
    pad.addstr(curr, 3, '-' * 41)
    return curr


def battery(pad):
    curr = 4
    pad.addstr(curr, 45, "Battery status      ")
    curr += 2
    stat = psutil.sensors_battery()
    if stat.power_plugged:
        pad.addstr(curr, 46, "Charger plugged in")
        pad.addstr(curr + 2, 46, "Battery charged:   " + str(stat.percent) + '% ')
        bar_length = int((int(stat.percent) / 100) * 20)
        for i in range(20):
            if i <= bar_length:

                pad.addch(curr + 2, 70 + i, ' ', curses.A_STANDOUT)
            else:
                pad.addch(curr + 1, 70 + i, ' ', curses.A_UNDERLINE)
                pad.addch(curr + 2, 70 + i, ' ', curses.A_UNDERLINE)
        pad.addch(curr + 2, 90, '|')
        curr += 4
        pad.addstr(curr, 45, '-' * 47)

    else:
        pad.addstr(curr, 46, "On Battery          ")
        pad.addstr(curr + 2, 46, "Battery Remaining: " + str(stat.percent) + '%' + ' ')
        bar_length = int((int(stat.percent) / 100) * 20)
        for i in range(20):
            if i <= bar_length:
                pad.addch(curr + 2, 70 + i, ' ', curses.A_STANDOUT)
            else:
                pad.addch(curr + 1, 70 + i, ' ', curses.A_UNDERLINE)
                pad.addch(curr + 2, 70 + i, ' ', curses.A_UNDERLINE)
        pad.addch(curr + 2, 90, '|')
        pad.addstr(curr + 4, 46, "Estimated Time: " + str(stat.secsleft / 60) + ' min')
        curr += 4
        pad.addstr(curr, 45, '-' * 47)
    return curr


def netio(pad, curr):
    curr += 2
    pad.addstr(curr, 45, "Network stats")
    curr += 2

    # Calculating upload and download speeds

    ini = psutil.net_io_counters()
    t_i = time.time()
    ini_s = ini.bytes_sent
    ini_r = ini.bytes_recv
    sleep(1)
    fin = psutil.net_io_counters()
    fin_s = fin.bytes_sent
    fin_r = fin.bytes_recv
    t_f = time.time()
    upload_speed = str((fin_s - ini_s) / (t_f - t_i))[:10]
    download_speed = str((fin_r - ini_r) / (t_f - t_i))[:10]
    upload_speed += ' ' * (10 - len(upload_speed))
    download_speed += ' ' * (10 - len(download_speed))
    pad.addstr(curr, 46, "Upload Speed: " + upload_speed + " kb/s")
    pad.addstr(curr + 2, 46, "Download Speed: " + download_speed + " kb/s")
    curr += 4
    pad.addstr(curr, 45, '-' * 47)
    curr += 2
    pad.refresh()
    return curr


def secondry_mem(pad, curr):
    curr += 2
    pad.addstr(curr, 45, "System disks stats    ")
    curr += 2

    # Calculating upload and download speeds

    ini = psutil.disk_io_counters()
    t_i = time.time()
    ini_s = ini.read_bytes
    ini_r = ini.write_bytes
    sleep(1)
    fin = psutil.disk_io_counters()
    fin_s = fin.read_bytes
    fin_r = fin.write_bytes
    t_f = time.time()
    upload_speed = str((fin_s - ini_s) / (t_f - t_i))[:10]
    download_speed = str((fin_r - ini_r) / (t_f - t_i))[:10]
    upload_speed += ' ' * (10 - len(upload_speed))
    download_speed += ' ' * (10 - len(download_speed))
    pad.addstr(curr, 46, "Read Speed: " + upload_speed + " kb/s")
    pad.addstr(curr + 2, 46, "Write Speed: " + download_speed + " kb/s")
    curr += 4
    pad.addstr(curr, 45, '-' * 47)
    curr += 2
    return curr


def cpu_graph(pad):
    curr = 2
    pad.addstr(curr, 95, "CPU graph")
    curr += 2
    dq = [0] * 30  # queue of length 30 i,e. stores previous 30 values
    curr += 20
    while True:
        per = psutil.cpu_percent()
        pad.addstr(curr - 21, 95, 'Current Usage: ' + str(per) + '%')
        dq.append(int((int(per) * 20) / 100))
        # print(dq)
        dq.pop(0)
        prev = dq[0]
        # print(curr)

        for row in range(95, 125):
            # print(prev,dq[row-95])
            for col in range(21):
                if dq[row - 95] < prev:
                    if col == dq[row - 95]:
                        pad.addch(curr - col, row, "_", curses.A_BOLD)
                    else:
                        pad.addch(curr - col, row, ' ')
                elif dq[row - 95] == prev:
                    if col == dq[row - 95]:

                        pad.addch(curr - col, row, '_', curses.A_BOLD)
                    else:
                        pad.addch(curr - col, row, ' ')
                else:
                    if prev <= col <= dq[row - 95]:
                        pad.addch(curr - col, row, '_', curses.A_BOLD)
                    else:
                        pad.addch(curr - col, row, ' ')
            prev = dq[row - 95]
        pad.addstr(curr+3, 95, '-'*30)
        pad.refresh()
        print(EXIT)
        if EXIT:
            exit()
        if pad.getch() > 0:
            exit()
        sleep(1)


def main_mem_graph(pad):
    curr = 2
    pad.addstr(curr, 130, "Main Memory graph")
    curr += 2
    dq = [0] * 30  # queue of length 30 i,e. stores previous 30 values
    curr += 20
    while True:
        per = psutil.virtual_memory().percent
        pad.addstr(curr - 21, 130, 'Current Usage: ' + str(per) + '%')
        dq.append(int((int(per) * 20) / 100))
        # print(dq)
        dq.pop(0)
        prev = dq[0]
        # print(curr)

        for row in range(130, 160):
            # print(prev,dq[row-95])
            for col in range(21):
                if dq[row - 130] <= prev:
                    if col == dq[row - 130]:
                        pad.addch(curr - col, row, "_",curses.A_BOLD)
                    else:
                        pad.addch(curr - col, row, ' ')
                else:
                    if prev <= col <= dq[row - 130]:
                        pad.addch(curr - col, row, '_', curses.A_BOLD)
                    else:
                        pad.addch(curr - col, row, ' ')
            prev = dq[row - 130]
        pad.addstr(curr+3, 130, '-'*30)
        pad.refresh()
        print(EXIT)
        if EXIT:
            exit()
        if pad.getch() > 0:
            exit()
        sleep(1)


def main(stdscr):
    try:
        stdscr.addch(40, 60, ' ')
    except:
        print("Screen size not enough...")
        exit()
    curses.curs_set(0)
    stdscr.scrollok(True)
    stdscr.idlok(True)
    pad = stdscr
    pad.nodelay(True)
    pad.addstr(1, 2, 'RESOURCE MONITOR', curses.A_DIM)
    print(stdscr.getch(1, 2))
    pad.addstr(3, 2, 'CPU STATS')
    pad.addstr(4, 3, 'CPU USAGE')
    pad.refresh()

    cpu_gr = Thread(target=cpu_graph, args=(pad,))
    mm_gr = Thread(target=main_mem_graph, args=(pad, ))
    cpu_gr.start()
    mm_gr.start()
    while True:
        row = cpu(pad)
        row = main_mem(pad, row)
        row = battery(pad)
        net_thread = Thread(target=netio, args=(pad, 10,))
        sec_mem_thread = Thread(target=secondry_mem, args=(pad, 19,))
        net_thread.start()
        sec_mem_thread.start()
        pad.refresh()
        sleep(0.1)
        if pad.getch() > 0:
            EXIT = True
            cpu_gr.join()
            mm_gr.join()
            os._exit(0)


curses.wrapper(main)
