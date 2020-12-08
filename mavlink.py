import os
from pymavlink import mavutil
import time

# master = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
master = mavutil.mavlink_connection('udpout:0.0.0.0:14550')

master.wait_heartbeat()

# Get some information !
while True:
	try:
		print(master.recv_match().to_dict())
	except:
		pass
	time.sleep(0.1)