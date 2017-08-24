# -*- coding: utf-8 -*-
from FanModule import *
from CPUModule import *
from PM8060Module import *
import os
import sys
import time
import threading

try:
    file_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    file_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(file_dir)

start_time = 0
# global variables
app_status = 's'  # available value: stopped(s) running(r) stopped2start(s2s) running2stopped(r2s)
status_lock = threading.Lock()  # lock between monitor and scheduler


# task to tune fan speed
def task2tune_fan():
    set_as_manual()  # set fan control mode as manual
    duration = time.time()- start_time
    for key in ["100", "90", "80", "70", "60", "50", "40", "30", "20", "10", "0"]:
        while int(duration) <= int(config["step_para"][key]["time"]):
            if app_status == 'r':
                time.sleep(1)
                duration = time.time() - start_time
            elif app_status == 's':
                set_as_auto()
                return
            else:
                break
        if app_status == 'r':
            set_fan_speed(config["step_para"][key]["speed"])
        else:
            break


# task to tune cpu utilization
def task2tune_cpu():
    global start_time
    duration = time.time() - start_time
    for key in ["100", "90", "80", "70", "60", "50", "40", "30", "20", "10", "0"]:
        while int(duration) <= int(config["step_para"][key]["time"]):
            if app_status == 'r':
                time.sleep(1)
                duration = time.time() - start_time
            elif app_status == 's':
                set_processor_value(0, 100)
                return
            else:
                break
        if app_status == 'r':
            set_processor_value(config["step_para"][key]["cpu"]["min"], config["step_para"][key]["cpu"]["max"])
        else:
            break


def task2tune_pm8060():
    global start_time
    global app_status
    duration = time.time() - start_time
    while int(duration) <= int(config["pm8060"]["time"]):
        if app_status == 'r':
            time.sleep(1)
            duration = time.time() - start_time
        elif app_status == 's':
                restore_pm8060()
                return
        else:
            break
    for volume in config["pm8060"]["ld"].keys():
        if app_status == 'r':
            pm8060_power_saving(volume)
        else:
            break
            
        
def task2tune_disk():
    global start_time
    global app_status
    duration = time.time() - start_time
    while int(duration) <= int(config["disk"]["time"]):  # wait
        if app_status == 'r':
            time.sleep(1)
            duration = time.time() - start_time
        elif app_status == 's':
            return 
        else:
            break
    for key in config['disk']['dev'].keys():
        if config['disk']['dev'][key]['type'] == 'sata':
            sata_sleep(config['disk']['dev'][key]['label'])
        elif config['disk']['dev'][key]['type'] == 'sas':
            sas_sleep(config['disk']['dev'][key]['label'])
        else:
            pass
            
            
def task2tune_uncore():
    duration = time.time()- start_time
    for key in ["100", "90", "80", "70", "60", "50", "40", "30", "20", "10", "0"]:
        while int(duration) <= int(config["step_para"][key]["time"]):
            if app_status == 'r':
                time.sleep(1)
                duration = time.time() - start_time
            elif app_status == 's':
                set_uncore('1800')
                return
            else:
                break
        if app_status == 'r':
            set_uncore(config["step_para"][key]["uncore"])
        else:
            break


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


# task scheduler
def thread_scheduler():
    global app_status
    global start_time
    scheduler_func = {
        "fan": task2tune_fan,
        "cpu": task2tune_cpu,
        "pm8060": task2tune_pm8060,
        "disk": task2tune_disk,
        "uncore": task2tune_uncore
    }
    while True:
        if status_lock.acquire():
            if DEBUG:
                print("I got it!")
            if app_status == 's2r':  # stopped to run
                app_status = 'r'
                start_time = time.time()
                thread_n = {}
                for key in config["switch"].keys():
                    if config["switch"][key] == "on":
                        thread_n[key] = "thread_%s" % key
                        thread_n[key] = threading.Thread(target=scheduler_func[key])
                        thread_n[key].setDaemon(True)
                        thread_n[key].start()
                        if DEBUG:
                            print("%s has been started!" % scheduler_func[key])
            elif app_status == 'r2s':
                app_status = 's'
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
        pid0 = check_app_status("java.exe", "SpecPowerSsj")  # get app status
        if pid0 != -1:  # app is running
            app_status_new = 'r'
        else:  # app is stopped
            app_status_new = 's'
        if app_status_old == 's' and app_status_new == 's':
            app_status = 's'
        elif app_status_old == 's' and app_status_new == 'r':
            app_status = 's2r'
        elif app_status_old == 'r' and app_status_new == 'r':
            app_status = 'r'
        elif app_status_old == 'r' and app_status_new == 's':
            app_status = 'r2s'
        if DEBUG:
            print("SpecPower running status is: %s" % app_status)
        app_status_old = app_status_new  # update app_status_old value
        status_lock.release()
        time.sleep(5)

