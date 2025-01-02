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
print("Heartbeat received, system is alive!")

MESSAGE_ID = 224 

# Send a COMMAND_LONG message to request the EXTENDED_SYS_STATE message
connection.mav.command_long_send(
    connection.target_system,
    0,  # Target component (use 0 to target all components)
    mavutil.mavlink.MAV_CMD_DO_SET_MISSION_CURRENT,
    1,  # Confirmation
    4, 0, 0, 0, 0, 0, 0  # Unused parameters
)
print(f"Request for message ID {MESSAGE_ID} sent")

print_specific_message(connection , "MISSION_CURRENT")