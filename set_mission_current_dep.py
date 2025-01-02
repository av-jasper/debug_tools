from pymavlink import mavutil
from mavlink_messages_utils import * 

# Connection string for MAVLink
connection_string = "udp:0.0.0.0:14551"
# Alternatively, you can use TCP
# connection_string = "tcp:av-quark-2.local:14550"

# Connect to MAVLink
connection = mavutil.mavlink_connection(connection_string)

# Wait for a heartbeat message to ensure connection
connection.wait_heartbeat()
mavlink_system_id = connection.target_system

target_component = 1  # Typically 1 for autopilot component
mission_type = mavutil.mavlink.MAV_MISSION_TYPE_MISSION

connection.mav.mission_set_current_send(
    mavlink_system_id,
    target_component,
    0,
)

# print_messages_for_one_second(connection)
