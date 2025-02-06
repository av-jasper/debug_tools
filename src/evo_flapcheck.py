from pymavlink import mavutil

# Connection string for MAVLink
connection_string = "tcp:10.41.0.1:5790"
# Alternatively, you can use TCP
# connection_string = "tcp:av-quark-2.local:14550"

# Connect to MAVLink
connection = mavutil.mavlink_connection(connection_string)

# Wait for a heartbeat message to ensure connection
connection.wait_heartbeat()
print("Heartbeat received, system is alive!")

collision = 247

# Send a COMMAND_LONG message to request the EXTENDED_SYS_STATE message
connection.mav.command_long_send(
    1,
    1,  # Target component (use 0 to target all components)
    collision,
    0,  # Confirmation
    2, 0, 0, 0, 0, 0, 0  # Unused parameters
)
