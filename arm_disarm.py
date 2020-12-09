"""
Example of how to Arm and Disarm an Autopilot with pymavlink
"""
# Import mavutil
from pymavlink import mavutil
import time

# Create the connection
vehicle = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
# vehicle = mavutil.mavlink_connection('udpin:0.0.0.0:14550')



# Arm
# vehicle.arducopter_arm()
# armed = vehicle.motors_armed()
# print(armed)


# master.mav.command_long_send(
#     master.target_system,
#     master.target_component,
#     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
#     0,
#     1, 0, 0, 0, 0, 0, 0)

# Disarm
# master.arducopter_disarm()
# master.mav.command_long_send(
#     master.target_system,
#     master.target_component,
#     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
#     0,
#     0, 0, 0, 0, 0, 0, 0)