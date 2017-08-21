from lib import printf
from common import *
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
        return False


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
        return False


def task_tune_disk(status_queue, duration_queue):
    while int(duration_queue.get()) < int(config['disk_param']['time']):
        if status_queue.get() == 's':  # if spec power stopped, return
            return
        time.sleep(1)
    for key in config['disk_param']['disk'].keys():
        if config['disk_param']['disk'][key]['type'] == 'sata':
            sata_sleep(config['disk_param']['disk'][key]['label'])
        elif config['disk_param']['disk'][key]['type'] == 'sas':
            sas_sleep(config['disk_param']['disk'][key]['label'])
        else:
            pass
        if status_queue.get() == 's':  # if spec power stopped, return
            return

