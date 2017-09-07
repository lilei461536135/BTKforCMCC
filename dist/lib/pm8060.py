# -*- coding: utf-8 -*-
from GlobalVars import *
import subprocess
import os

controller_id = config["pm8060"]["controller_id"]


# get HDD status(optimal, raw or ready)
def get_hdd_status(channel, device):
    cmd = "%s getconfig %s pd" % (arcconf, controller_id)
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pid.communicate()
    i = 0
    for line in out.decode().split(os.linesep):
        if line.find("Device is a Hard drive") >= 0:
            location_line = out.decode().split(os.linesep)[i+6]
            state_line = out.decode().split(os.linesep)[i+1]
            if location_line.find("Reported Channel,Device(T:L)") >= 0 and location_line.find("%s,%s" % (channel, device)) >= 0:
                if state_line.find("Raw") >= 0:
                    state = "Raw"
                    return state
                elif state_line.find("Ready") >= 0:
                    state = "Ready"
                    return state
                elif state_line.find("Online"):
                    state = "Online"
                    return state
        i += 1
    return False


# get logical devices' id for setting
# name: logical drive name
# return code: logical devices' id or -1
def get_ld_id2set(name):
    cmd = "%s getconfig %s ld" % (arcconf, controller_id)
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pid.communicate()
    i = 0
    for line in out.decode().split(os.linesep):
        if line.find(name) >= 0:
            num_line = out.decode().split(os.linesep)[i - 1]
            id_id = num_line.strip()[22]
            return id_id
        i += 1
    return -1


# PM8060 Power Saving
def pm8060_power_saving(volume):
    ch = config["pm8060"]["ld"][volume]["channel"]  # channel
    i = config["pm8060"]["ld"][volume]["id"]  # id
    s = config["pm8060"]["ld"][volume]["size"]
    state = get_hdd_status(ch, i)
    if state == "Raw":
        printf("Initialize Device On controller %s channel %s id %s" % (controller_id, ch, i))
        cmd = "%s task start %s device %s %s initialize noprompt" % (arcconf, controller_id, ch, i)
        try:
            pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            out, err = pid.communicate()
            printf(out.decode())
            printf(err.decode())
        except Exception as e:
            printf(e)
    if not check_ld_status(volume):
        printf("Create Volume On controller %s channel %s id %s" % (controller_id, ch, i))
        cmd = "%s create %s LOGICALDRIVE  name %s %s Simple_Volume %s %s noprompt" % \
              (arcconf, controller_id, volume, s, ch, i)
        pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = pid.communicate()
        printf(out.decode())
        printf(err.decode())
    printf("Set Logical Drive %s as poweroff mode" % volume)
    device_id = get_ld_id2set(volume)
    cmd = "%s setpower %s LD %s poweroff 3" % (arcconf, controller_id, device_id)
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pid.communicate()
    printf(out.decode())
    printf(err.decode())


def check_ld_status(volume):
    cmd = "%s getconfig %s ld" % (arcconf, controller_id)
    pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = pid.communicate()
    for line in out.decode().split(os.linesep):
        if line.find(volume) >= 0:
            return True
    return False


# Restore PM8060
def restore_pm8060():
    for volume in config["pm8060"]["ld"].keys():
        if check_ld_status(volume):
            printf("Delete logical drive %s" % volume)
            device_id = get_ld_id2set(volume)
            cmd = "%s delete %s LOGICALDRIVE %s noprompt" % (arcconf, controller_id, device_id)
            pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            pid.wait()
    for volume in config["pm8060"]["ld"].keys():
        if not check_ld_status(volume):
            ch = config["pm8060"]["ld"][volume]["channel"]  # channel
            i = config["pm8060"]["ld"][volume]["id"]  # id
            printf("Uninitialize Device On controller %s channel %s id %s" % (controller_id, ch, i))
            cmd = "%s uninit %s %s %s" % (arcconf, controller_id, ch, i)
            pid = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            pid.wait()

            
def task2tune_pm8060(app_status, start_time):
    duration = time.time() - start_time[0]
    while int(duration) <= int(config["pm8060_param"]["time"]):
        if app_status[0] == 'r':
            time.sleep(1)
            duration = time.time() - start_time[0]
        elif app_status[0] == 's':
                restore_pm8060()
                return
        else:
            break
    for volume in config["pm8060_param"]["ld"].keys():
        if app_status[0] == 'r':
            pm8060_power_saving(volume)
        else:
            break            