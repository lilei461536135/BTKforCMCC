# -*- coding: utf-8 -*-
import json
import os
import sys

# get JSON configuration data
with open('config.json', 'r') as f:
    config = json.load(f)
    f.close()

# get file located path
try:
    file_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:  # We are the main py2exe script, not a module
    file_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

ipmitool = file_dir + "\winipmitool-1.8.7\ipmitool.exe"
sg_start = file_dir + "\Sg3_Utils\sg_start.exe"
sg_sat_set_features = file_dir + "\Sg3_Utils\sg_sat_set_features.exe"


