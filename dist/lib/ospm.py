# -*- coding: utf-8 -*-
import subprocess
import time
from lib.globalvars import *


def set_as_balance():
    printf("Set OS Power Management plan to Balanced")
    cmd = "powercfg.exe -setactive 381b4222-f694-41f0-9685-ff5bb260df2e"
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        printf("set os power management plan to performance failed!")
        printf(e)
        
    
def set_as_performance():
    printf("Set OS Power Management plan to Performance")
    cmd = "powercfg.exe -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        printf("set os power management plan to performance failed!")
        printf(e)    
        
        
def task2tune_ospm(app_status, start_time):
    duration = time.time() - start_time[0]
    while int(duration) <= int(config['ospm_param']['time']):  # wait
        if app_status[0] == 'r':
            time.sleep(1)
            duration = time.time() - start_time[0]
        elif app_status[0] == 's':
            set_as_balance()  # restore
            return 
        else:
            break
    set_as_performance()
    while app_status[0] != 's':
        time.sleep(5)
    set_as_balance()  # restore