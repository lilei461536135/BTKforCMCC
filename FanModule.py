# -*- coding: utf-8 -*-
from GlobalVars import *
import subprocess
import sys
mode_cmd = config["fan"]["mode_cmd"]
speed_cmd = config["fan"]["speed_cmd"]


def set_as_manual():
    # set fan control mode as manual
    if DEBUG:
        print("set fan control mode as manual")
    cmd = "%s wmi raw %s 0x01" % (ipmitool, mode_cmd)
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        if DEBUG:
            print("set fan control mode as manual failed")
            print(e)
        return False


def set_as_auto():
    # set fan control mode as auto
    if DEBUG:
        print("set fan control mode as auto")
    cmd = "%s wmi raw %s 0x00" % (ipmitool, mode_cmd)
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        if DEBUG:
            print("set fan control mode as auto failed")
            print(e)
        return False


def set_fan_speed(value):
    try:
        # set fan speed
        if DEBUG:
            print("set fan speed to %s" % value)
        cmd = "%s wmi raw %s 0xff %s" % (ipmitool, speed_cmd, value)
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        if DEBUG:
            print("set fan speed failed")
            print(e)
        sys.exit(-1)
