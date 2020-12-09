"""
Example of how to Arm and Disarm an Autopilot with pymavlink
"""
# Import mavutil
from pymavlink import mavutil
import time

# Create the connection
vehicle = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
# vehicle = mavutil.mavlink_connection('udpin:0.0.0.0:14550')