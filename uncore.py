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

