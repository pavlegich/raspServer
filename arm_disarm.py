"""
Example of how to Arm and Disarm an Autopilot with pymavlink
"""
# Import mavutil
from pymavlink import mavutil

# Create the connection
vehicle = mavutil.mavlink_connection("/dev/ttyACM0", baud=115200)
# vehicle = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
# Wait a heartbeat before sending commands
vehicle.wait_heartbeat()

# GPS



status = vehicle.messages('GPS_RAW_INT')
print(status)

# location = vehicle.location()
# print(location.lat)
# print(location.lng)
# print(location.alt)

# https://mavlink.io/en/messages/common.html#MAV_CMD_COMPONENT_ARM_DISARM

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