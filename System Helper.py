# -*- coding: utf-8 -*-
from common import *
from lib import printf
import multiprocessing
from multiprocessing import Queue
import time
import subprocess
from fan import task_tune_fan
from disk import task_tune_disk
from uncore import task_tune_uncore


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
def process2record_status(queue):
    app_status = 's'  # app status, s: stopped r: running s2r: stopped2run
    status_old = 's'
    while True:
        # pid0 = check_app_status("java.exe", "SpecPowerSsj")  # get app status
        pid0 = check_app_status("java.exe", "SpecPowerSsj")
        if pid0 != -1:  # app is running
            status_new = 'r'
        else:  # app is stopped
            status_new = 's'
        if status_old == 's' and status_new == 's':
            app_status = 's'
        elif status_old == 's' and status_new == 'r':
            app_status = 's2r'
        elif status_old == 'r' and status_new == 'r':
            app_status = 'r'
        elif status_old == 'r' and status_new == 's':
            app_status = 's'
        else:
            pass
        printf("APP status is %s" % app_status)
        if queue.empty():
            queue.put(app_status)
        status_old = status_new
        time.sleep(1)


# Task manager
def task_manager(queue_status):
    app_start_time = 0
    app_duration = 0
    task_func = {
        "fan": task_tune_fan,
        "uncore": task_tune_uncore,
        "disk": task_tune_disk
    }
    pid = {}
    queue1 = {}
    queue2 = {}
    for key in config['switch'].keys():
        if config['switch'][key] == 'on':
            pid[key] = "pid_" + key
            queue1[key] = "queue1_" + key
            queue1[key] = Queue(1)
            queue2[key] = "queue2_" + key
            queue2[key] = Queue(1)
    while True:
        status = queue_status.get()  # block mode
        if status == 's2r':
            app_start_time = time.time()
            for key in pid.keys():
                pid[key] = multiprocessing.Process(target=task_func[key], args=(queue1[key], queue2[key]))
                pid[key].daemon = True
                pid[key].start()
        elif status == 'r':
            app_duration = int(time.time()) - int(app_start_time)
        elif status == 's':
            app_start_time = 0
            app_duration = 0
        # update app status and app duration
        for key in pid.keys():
            if not queue1[key].empty():  # clear
                queue1[key].get()
            queue1[key].put(status)
            if not queue2[key].empty():  # clear
                queue2[key].get()
            queue2[key].put(app_duration)

# main function
if __name__ == "__main__":
    # variables
    status_queue = Queue(1)  # has only one number
    # change work directory
    os.chdir(file_dir)
    #
    printf("Start to monitor app status")
    p = multiprocessing.Process(target=process2record_status, args=(status_queue,))
    p.daemon = True
    p.start()
    task_manager(status_queue)
    printf("exit!")





