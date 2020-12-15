from pymavlink import mavutil
import time
from MAVProxy.modules.lib import mp_module


vehicle = mavutil.mavlink_connection('udpin:localhost:14550')

while True:
	vehicle.wait_heartbeat()
	lat = vehicle.messages["GPS_RAW_INT"].lat*1e-7
	lon = vehicle.messages["GPS_RAW_INT"].lon*1e-7
	alt = vehicle.messages["GPS_RAW_INT"].alt*1e-3
	sv = vehicle.messages['GPS_RAW_INT'].satellites_visible
	print(lat,lon,alt,sv)

# altitude = 3

# vehicle.mav.command_long_send(
# 	vehicle.target_system,  # target_system
# 	mavutil.mavlink.MAV_COMP_ID_SYSTEM_CONTROL, # target_component
# 	mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, # command
# 	0,0,0,0,0,0,0,altitude)