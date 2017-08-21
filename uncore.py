import subprocess
from common import *
from lib import printf
import time


def set_uncore(value):
    cmd = "%s -MSR WRITE 0x0 0x620 %s 0x0" % (h2orte, hex(int(value)))
    try:
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        pid.wait()
    except Exception as e:
        printf("Set disk %s to sleep failed!")
        printf(e)
        return False


def task_tune_uncore(status_queue, duration_queue):
    for key in sorted(config['uncore_param']['time_seq'].keys(), key=lambda a: int(a)):
        while int(duration_queue.get()) < int(config['uncore_param']['time_seq'][key]):  # waiting for shift speed
            if status_queue.get() == 's':  # if spec power stopped, return
                set_uncore(config['uncore_param']['default_val'])
                return
            time.sleep(1)
        set_uncore(config['uncore_param']['freq_seq'][key])

