# -*- coding: utf-8 -*-
import subprocess
from lib.globalvars import *
import time


def set_uncore(value):
    printf("Set Uncore Freq to %s00" % value)
    cmd = "%s -MSR WRITE 0x0 0x620 %s 0x0" % (h2orte, hex(value))
    printf(cmd)
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = pid.communicate()
        printf("output: %s" % out.decode())
        printf("error: %s " % err.decode())
    except Exception as e:
        printf("Set uncore value to %s failed!" % value)
        printf(e)
        
        
def task2tune_uncore(app_status, start_time):
    duration = time.time()- start_time[0]
    for key in sorted(config['step_param'].keys(), key=lambda a: int(a)):
        while int(duration) <= int(config["step_param"][key]["time"]):
            if app_status[0] == 'r':
                time.sleep(1)
                duration = time.time() - start_time[0]
            elif app_status[0] == 's':
                set_uncore(config['uncore_param']['default_val'])
                return
            else:
                break
        if app_status[0] == 'r':
            set_uncore(config["step_param"][key]["uncore"])
        else:
            break    
    while app_status[0] != 's':
        time.sleep(5)
    set_uncore(config['uncore_param']['default_val'])  # set uncore freq to default