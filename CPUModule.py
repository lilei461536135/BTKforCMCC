# -*- coding: utf-8 -*-
from GlobalVars import *
import subprocess


# set processor state value
def set_processor_value(min_value, max_value):
    if DEBUG:
        print("Set Minimum Processor State: %s" % min_value)
    # Minimum Processor State --> ?
    cmd = "powercfg.exe -setacvalueindex 381b4222-f694-41f0-9685-ff5bb260df2e 54533251-82be-4824-96c1-47b60b740d00 " \
          "893dee8e-2bef-41e0-89c6-b55d0929964c %s" % min_value
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    pid.wait()
    # Maximum Processor State --> ?
    if DEBUG:
        print("Set Maximum Processor State: %s" % max_value)
    cmd = "powercfg.exe -setacvalueindex 381b4222-f694-41f0-9685-ff5bb260df2e 54533251-82be-4824-96c1-47b60b740d00 " \
          "bc5038f7-23e0-4960-96da-33abaf5935ec %s" % max_value
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    pid.wait()
    # Set Configration active, Balanced Performance
    if DEBUG:
        print("Set Configration Active")
    cmd = "powercfg.exe -setactive 381b4222-f694-41f0-9685-ff5bb260df2e"
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    pid.wait()
