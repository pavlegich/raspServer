import os
from pymavlink import mavutil
import time

master = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
# master = mavutil.mavlink_connection('udp:0.0.0.0:14550')

master.wait_heartbeat()

# Get some information !
while True:
	try:
		altitude = master.messages['GPS_RAW_INT']  # Note, you can access message fields as attributes!
		timestamp = master.time_since('GPS_RAW_INT')
		print(altitude)
	except:
		print('No GPS_RAW_INT message received')