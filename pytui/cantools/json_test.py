#!/usr/bin/env python
import json

with open('D:\DCU15_IG\DB\GN7_M\\ECANFD_GN7_M.0.json', 'r') as f:
    json_data = json.load(f)

periodMessages = json_data['periodMessages']
print(periodMessages)

manualMessages = json_data['manualMessages']
print(manualMessages)