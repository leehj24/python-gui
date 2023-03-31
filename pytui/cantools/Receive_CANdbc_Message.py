#!/usr/bin/env python
import can
import cantools
from can.message import Message

db = cantools.db.load_file('D:/DCU15_IG/DB/GN7_M/ECANFD_GN7_M.0.dbc')

bus = can.interface.Bus(bustype = 'vector', channel = 0)
while True:
    message = bus.recv()
    print(db.decode_message(message.arbitration_id, message.data))