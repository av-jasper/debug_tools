from pymavlink import mavutil

# Connection string for MAVLink
connection_string = "udp:0.0.0.0:14551"
# Alternatively, you can use TCP
# connection_string = "tcp:av-quark-2.local:14550"

# Connect to MAVLink
connection = mavutil.mavlink_connection(connection_string)

# Wait for a heartbeat message to ensure connection
connection.wait_heartbeat()
print("Heartbeat received, system is alive!")


# Send a COMMAND_LONG message to request the EXTENDED_SYS_STATE message
connection.mav.command_long_send(
    connection.target_system,
    0,  # Target component (use 0 to target all components)
    mavutil.mavlink.MAV_CMD_DO_SET_MODE,
    0,  # Confirmation
    0, 0, 0, 0, 0, 0, 0  # Unused parameters
)

# Listen for the EXTENDED_SYS_STATE message
while True:
    # Wait for the next message
    msg = connection.recv_match(type="MISSION_CURRENT", blocking=True)

    
    if msg:
        data = msg.to_dict()
        
        # Print all fields
        for key, value in data.items():
            print(f"{key}: {value}")
    break