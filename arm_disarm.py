"""
Example of how to Arm and Disarm an Autopilot with pymavlink
"""
# Import mavutil
from pymavlink import mavutil, mavextra
import time

# Create the connection
vehicle = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
# vehicle = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

while True:
    vehicle.wait_heartbeat()
    lat = vehicle.messages["GPS_RAW_INT"].lat*1e-7
    lon = vehicle.messages["GPS_RAW_INT"].lon*1e-7
    alt = vehicle.messages["GPS_RAW_INT"].alt*1e-3
    new = mavextra.gps_newpos(lat, lon, 0, 10)
    print(new)

