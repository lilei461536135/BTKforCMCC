from common import *
from lib import printf
from lib import get_app_status
from lib import get_app_run_duration
import subprocess


def set_as_manual():
    # set fan control mode as manual
    printf("set fan control mode as manual")
    mode_cmd = config['fan_param']['mode_cmd']
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
    mode_cmd = config['fan_param']['mode_cmd']
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
        fan_num_seq = config['fan_param']['num_seq']
        for key in fan_num_seq.keys():
            printf("set fan %s speed to %s" % (fan_num_seq[key], value))
            speed_cmd = config['fan_param']['speed_cmd']
            cmd = "%s wmi raw %s %s %s" % (ipmitool, speed_cmd, key, value)
            pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            pid.wait()
    except Exception as e:
        printf("set fan speed failed")
        printf(e)
        sys.exit(-1)


def task_tune_fan():
    while True:
        if get_app_status() == 's':
            break
        for key in sorted(config['fan_param']['time_seq'].keys(), key=lambda a: int(a)):
            duration = get_app_run_duration()
            if int(duration) > int(config['fan_param']['time_seq'][key]):
                set_fan_speed(config['fan_param']['speed_seq'][key])
