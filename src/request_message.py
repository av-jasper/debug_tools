from pymavlink import mavutil

# MAVLink connection setup
connection_string = "tcp:10.41.0.1:5790"  # Adjust as needed
connection = mavutil.mavlink_connection(connection_string)

# Wait for heartbeat to confirm connection
print("Waiting for heartbeat...")
connection.wait_heartbeat()
print(f"Connected to system {connection.target_system} component {connection.target_component}")

# MAV_CMD_REQUEST_MESSAGE command parameters
MESSAGE_ID = 148  # AUTOPILOT_VERSION
REQ_PARAM_1 = 0  # Unused
REQ_PARAM_2 = 0  # Unused
REQ_PARAM_3 = 0  # Unused
REQ_PARAM_4 = 0  # Unused
REQ_PARAM_5 = 0  # Unused
RESPONSE_TARGET = 1  # Address of requestor

# Send the command to request the AUTOPILOT_VERSION message
connection.mav.command_long_send(
    1,
    1,
    mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
    0,  # Confirmation
    MESSAGE_ID,
    REQ_PARAM_1,
    REQ_PARAM_2,
    REQ_PARAM_3,
    REQ_PARAM_4,
    REQ_PARAM_5,
    RESPONSE_TARGET
)

print("Request sent. Waiting for response...")

# Wait for the AUTOPILOT_VERSION message
while True:
    msg = connection.recv_match(type='AUTOPILOT_VERSION', blocking=True, timeout=5)
    if msg:
        print(msg)
        break
    else:
        print("Timeout waiting for AUTOPILOT_VERSION message.")
        break
