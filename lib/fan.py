# -*- coding: utf-8 -*-
from lib.globalvars import *
import subprocess
import sys
import time
mode_cmd = config["fan_param"]["mode_cmd"]
speed_cmd = config["fan_param"]["speed_cmd"]


def set_as_manual():
    # set fan control mode as manual
    printf("set fan control mode as manual")
    cmd = "%s wmi raw %s 0x01" % (ipmitool, mode_cmd)
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        printf("set fan control mode as manual failed")
        printf(e)
        return False


def set_as_auto():
    # set fan control mode as auto
    printf("set fan control mode as auto")
    cmd = "%s wmi raw %s 0x00" % (ipmitool, mode_cmd)
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        printf("set fan control mode as auto failed")
        printf(e)
        return False


def set_fan_speed(value):
    try:
        # set fan speed
        printf("set fan speed to %s" % value)
        cmd = "%s wmi raw %s 0xff %s" % (ipmitool, speed_cmd, value)
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        printf("set fan speed failed")
        printf(e)
        sys.exit(-1)
        

# task to tune fan speed
def task2tune_fan(app_status, start_time):
    set_as_manual()  # set fan control mode as manual
    duration = time.time()- start_time[0]
    for key in sorted(config['step_param'].keys(), key=lambda a: int(a)):
        while int(duration) <= int(config["step_param"][key]["time"]):
            if app_status[0] == 'r':
                time.sleep(1)
                duration = time.time() - start_time[0]
            elif app_status[0] == 's':
                set_as_auto()
                return
            else:
                break
        if app_status[0] == 'r':
            set_fan_speed(config["step_param"][key]["speed"])
        else:
            break
    while app_status[0] != 's':
        time.sleep(5)
    set_as_auto()

