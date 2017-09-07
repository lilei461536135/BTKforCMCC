# -*- coding: utf-8 -*-
import os
import sys
import time
import re
import threading
import subprocess
from lib.globalvars import *
from lib.fan import task2tune_fan
from lib.disk import task2tune_disk
from lib.uncore import task2tune_uncore
from lib.ospm import task2tune_ospm
scheduler_func = {}
for key in config['tasks'].keys():
    scheduler_func[config['tasks'][key]] = 'task2tune_' + config['tasks'][key]

try:
    file_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    file_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(file_dir)

start_time = [0]  # important!!! Using list for transmit address
# global variables
app_status = ['s']  # available value: stopped(s) running(r) stopped2start(s2s) running2stopped(r2s)
status_lock = threading.Lock()  # lock between monitor and scheduler


# check app status, return process id or -1
def check_app_status(app, keyword):
    cmd = "wmic PROCESS where \"name like \'" + "%" + app + "%\'\" " + "GET CommandLine,ProcessId"
    printf("Executing %s" % cmd)
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pid.communicate()
    printf("Returned output: %s" % out.decode())
    printf("Returned error: %s" % err.decode())
    printf("searching %s from output" % keyword)
    if out.decode().find(keyword) >= 0:
        printf("%s has been found" % keyword)
        for line in out.decode().split(os.linesep):
            if line.find(keyword) >= 0:
                process_id = line.strip().split()[-1]
                printf("process id is %s" % process_id)
                return process_id
    else:
        printf("%s has not been found" % keyword)
        return -1


# task scheduler
def thread_scheduler():
    global app_status
    global start_time
    global scheduler_func
    while True:
        if status_lock.acquire():
            printf("I got it!")
            if app_status[0] == 's2r':  # stopped to run
                app_status[0] = 'r'
                start_time[0] = time.time()
                thread_n = {}
                for key in scheduler_func.keys():
                        thread_n[key] = "thread_%s" % key
                        thread_n[key] = threading.Thread(target=eval(scheduler_func[key]), args=(app_status, start_time))
                        thread_n[key].start()
                        printf("%s has been started!" % scheduler_func[key])
            elif app_status[0] == 'r2s':
                app_status[0] = 's'
            else:
                pass
            # release thread lock
            status_lock.release()
        time.sleep(1)

if __name__ == "__main__":
    app_status_old = 's'  # init status: stopped
    # thread to schedule
    thread2 = threading.Thread(target=thread_scheduler)
    thread2.setDaemon(True)
    thread2.start()
    # monitor app status, update every 5 seconds
    while status_lock.acquire():
        pid0 = check_app_status(config['target']['app'], config['target']['keyword'])  # get app status
        if pid0 != -1:  # app is running
            app_status_new = 'r'
        else:  # app is stopped
            app_status_new = 's'
        if app_status_old == 's' and app_status_new == 's':
            app_status[0] = 's'
        elif app_status_old == 's' and app_status_new == 'r':
            app_status[0] = 's2r'
        elif app_status_old == 'r' and app_status_new == 'r':
            app_status[0] = 'r'
        elif app_status_old == 'r' and app_status_new == 's':
            app_status[0] = 'r2s'
        printf("%s running status is: %s" % (config['target']['app'], app_status[0]))
        app_status_old = app_status_new  # update app_status_old value
        status_lock.release()
        time.sleep(5)

