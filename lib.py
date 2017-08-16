# -*- coding: utf-8 -*-
from common import *

app_run_duration = 0
app_status = 's'


# print function with switch
def printf(string):
    if config['print'] == 'on':
        print(string)


# update current app status
def update_app_status(status):
    global app_status
    app_status = status


# return current app status
def get_app_status():
    global app_status
    return app_status


# update app running duration
def update_app_run_duration(dur):
    global app_run_duration
    app_run_duration = dur
