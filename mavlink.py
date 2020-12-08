from pymavlink import mavutil
import time

master = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)

while True:
	try:
		master.wait_heartbeat()
		lat = master.messages['GPS_RAW_INT'].lat*1e-7  # Note, you can access message fields as attributes!
		lon = master.messages['GPS_RAW_INT'].lon*1e-7
		alt = master.messages['GPS_RAW_INT'].alt*1e-3
	except:
		print('No GPS_RAW_INT message received')