# -*- coding: utf-8 -*-
import json

# get JSON config data
with open('config.json', 'r') as f:
    config = json.load(f)
    f.close()
ipmitool = "winipmitool-1.8.7\ipmitool.exe"
sg_start = "Sg3_Utils\sg_start.exe"
sg_sat_set_features = "Sg3_Utils\sg_sat_set_features.exe"
h2orte = "C:\Program Files (x86)\Insyde\H2ORTE-x64\H2ORTE-Wx64.exe"

# print function with switch
def printf(string):
    if config['print'] == 'on':
        print(string)



