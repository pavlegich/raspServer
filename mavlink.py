import os
from pymavlink import mavutil
import time

master = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
# master = mavutil.mavlink_connection('udp:0.0.0.0:14550')

master.wait_heartbeat()

# Get some information !
while True:
	try:
		lat = master.messages['GPS_RAW_INT'].lat*1e-7  # Note, you can access message fields as attributes!
		lon = master.messages['GPS_RAW_INT'].lon*1e-7
		alt = master.messages['GPS_RAW_INT'].alt*1e-3
		latG = master.messages['GLOBAL_POSITION_INT'].lat*1e-7
		print(lat)
		print(lon)
		print(alt)
		print(latG)
	except:
		print('No GPS_RAW_INT message received')
	time.sleep(1)