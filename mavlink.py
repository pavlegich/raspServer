import os
from pymavlink import mavutil 

master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

# Get some information !
while True:
	try:
		print(master.recv_match().to_dict())
	except:
		pass
	time.sleep(0.1)