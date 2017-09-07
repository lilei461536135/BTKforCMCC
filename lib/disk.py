# -*- coding: utf-8 -*-
from lib.globalvars import *
import time
import subprocess


# set sata disk to sleep
def sata_sleep(disk):
    printf("Set disk %s to sleep" % disk)
    try:
        cmd = "%s -f 4ah -c 00h -L 4h %s -vvvv" % (sg_sat_set_features, disk)
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
        cmd = "%s -f 4ah -c 00h -L 4h %s -vvvv"
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        printf("Set disk %s to sleep failed!")
        printf(e)


# set sas disk to sleep
def sas_sleep(disk):
    printf("Set disk %s to sleep" % disk)
    cmd = "%s -p 3h -m 0h %s -vvvv" % (sg_start, disk)
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        printf("Set disk %s to sleep failed!")
        printf(e)
        

def task2tune_disk(app_status, start_time):
    duration = time.time() - start_time[0]
    while int(duration) <= int(config['disk_param']['time']):  # wait
        if app_status[0] == 'r':
            time.sleep(1)
            duration = time.time() - start_time[0]
        elif app_status[0] == 's':
            return 
        else:
            break
    for key in config['disk_param']['dev'].keys():
        if config['disk_param']['dev'][key]['type'] == 'sata':
            sata_sleep(config['disk_param']['dev'][key]['label'])
        elif config['disk_param']['dev'][key]['type'] == 'sas':
            sas_sleep(config['disk_param']['dev'][key]['label'])
        else:
            pass        


