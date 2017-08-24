# -*- coding: utf-8 -*-
import json

DEBUG = 1
# get JSON config data
with open('config.json', 'r') as f:
    config = json.load(f)
    f.close()
ipmitool = "winipmitool-1.8.7\ipmitool.exe"
arcconf = "arcconf\\arcconf.exe"
