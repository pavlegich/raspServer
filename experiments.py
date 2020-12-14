from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

aTargetAltitude = 1

vehicle = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
print("Arming motors")
vehicle.arducopter_arm()
# vehicle.motors_armed_wait()
while vehicle.motors_armed():
	time.sleep(1)
print("Motors armed!")
time.sleep(10)

vehicle.arducopter_disarm()
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






