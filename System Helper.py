# -*- coding: utf-8 -*-
from common import *
from lib import printf
from lib import update_app_run_duration
from lib import update_app_status
import multiprocessing
from multiprocessing import Queue
import time
import subprocess

# global variables
current_time = 0
app_start_time = 0
app_duration = 0
status_queue = Queue(0)
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
    p = multiprocessing.Process(target=thread2update_time)
    p.daemon = True
    p.start()


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
def thread2record_status(queue):
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
        elif status_old == 's' and status_new == 'r':
            app_status = 's2r'
        elif status_old == 'r' and status_new == 'r':
            app_status = 'r'
        elif status_old == 'r' and status_new == 's':
            app_status = 'r2s'
        else:
            pass
        printf("APP status is %s" % app_status)
        queue.put(app_status)
        time.sleep(3)


# Initialize app status recorder
def init_status_recorder():
    printf("Initialize app status recorder")
    p = multiprocessing.Process(target=thread2record_status, args=(status_queue,))
    p.daemon = True
    p.start()


def task_tune_disk():
    print("helo")


def task_tune_uncore():
    print("helo")


def task_tune_fan():
    print("helo")


# Task manager
def task_manager(queue):
    global app_start_time
    global current_time
    global app_duration
    task_func = {
        "fan": task_tune_fan,
        "uncore": task_tune_uncore,
        "disk": task_tune_disk
    }
    while True:
        status = queue.get()
        update_app_status(app_status)
        if status == 's2r':
            app_start_time = time.time()
            pid = {}
            for key in config['switch'].keys():
                if config['switch'][key] == 'on':
                    pid[key] = "pid_" + key
                    pid[key] = multiprocessing.Process(target=task_func[key])
                    pid[key].daemon = True
                    pid[key].start()
        elif status == 'r':
            app_duration = int(current_time) - int(app_start_time)
            update_app_run_duration(app_duration)
        elif status == 's':
            app_start_time = 0
            app_duration = 0
            update_app_run_duration(app_duration)
        time.sleep(1)

# main function
if __name__ == "__main__":
    os.chdir(file_dir)
    init_clock()
    init_status_recorder()
    task_manager(status_queue)


