from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

aTargetAltitude = 1

vehicle = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
print("Arming motors")
vehicle.mav.command_long_send(
	vehicle.target_system,  # target_system
	vehicle.target_component,
	mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, # command
	0, # confirmation
	1, # param1 (1 to indicate arm)
	0, # param2 (all other params meaningless)
	0, # param3
	0, # param4
	0, # param5
	0, # param6
	0) # param7
# vehicle.motors_armed_wait()
while vehicle.motors_armed():
	time.sleep(1)
print("Motors armed!")
time.sleep(10)

vehicle.arducopter_disarm()
while not vehicle.motors_armed():
	time.sleep(1)
print("Motors disarmed!")
# print("Taking off!")
# vehicle.simple_takeoff(aTargetAltitude)
# time.sleep(10)
# print("Now let's land")
# vehicle.mode = VehicleMode("LAND")
# vehicle.close()

# REQUESTS

# import requests
# from requests.auth import HTTPDigestAuth

# i = 0
# ip = ['192.168.43.210','192.168.43.210']
# login = [['admin','admin'],['admin','admin']]
# url = 'http://' + ip[i] + ':5000/status'
# auth = HTTPDigestAuth(login[i][0], login[i][1])
# r = requests.get(url = url, auth = auth)
# data = r.json()

# lat = data['lat']
# lon = data['lon']
# alt = data['alt']

# print(lat,lon,alt)






