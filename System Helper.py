# -*- coding: utf-8 -*-
from printf import printf
from common import *
import multiprocessing
import time
import subprocess
import queue

# global variables
current_time = 0
status_queue = queue.Queue()
app_status = 's'  # app status, s: stopped r: running s2r: stopped2run r2s: run2stopped


# thread to update time
def thread2update_time():
    global current_time
    while True:
        current_time = time.time()
        time.sleep(1)


# Initialize Clock, update every 1s
def init_clock():
    printf("Initialize clock")
    multiprocessing.Process(target=thread2update_time).daemon(True).start()


# check app status, return process id or -1
def check_app_status(app, keyword):
    cmd = "wmic PROCESS where \"name like \'" + "%" + app + "%\'\" " + "GET CommandLine,ProcessId"
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pid.communicate()
    if out.decode().find(keyword) >= 0:
        for line in out.decode().split(os.linesep):
            if line.find(keyword) >= 0:
                process_id = line.strip().split()[-1]
                return process_id
    else:
        return -1


# get app status
def thread2record_status():
    global app_status
    status_new = 's'
    status_old = 's'
    while True:
        pid0 = check_app_status("java.exe", "SpecPowerSsj")  # get app status
        if pid0 != -1:  # app is running
            status_new = 'r'
        else:  # app is stopped
            status_old = 's'
        if status_old == 's' and status_new == 's':
            app_status = 's'
            status_queue.put(app_status)
        elif status_old == 's' and status_new == 'r':
            app_status = 's2r'
            status_queue.put(app_status)
        elif status_old == 'r' and status_new == 'r':
            app_status = 'r'
            status_queue.put(app_status)
        elif status_old == 'r' and status_new == 's':
            app_status = 'r2s'
        else:
            pass
        printf("APP status is %s" % app_status)
        status_queue.put(app_status)
        time.sleep(2)


# Initialize app status recorder
def init_recorder():
    printf("Initialize app status recorder")
    multiprocessing.Process(target=thread2record_status).daemon(True).start()


# Task trigger
def task_trigger():


# main function
if __name__ == "__main__":
    os.chdir(file_dir)
    init_clock()
    init_recorder()


