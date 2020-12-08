#!/usr/bin/python

import os
from pymavlink import mavutil 

master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

master.wait_heartbeat()

# while True:
# 	try:
# 		altitude = master.messages['GPS_RAW_INT']  # Note, you can access message fields as attributes!
# 		timestamp = master.time_since('GPS_RAW_INT')
# 		print(altitude)
#     except:
#     	print('No GPS_RAW_INT message received')