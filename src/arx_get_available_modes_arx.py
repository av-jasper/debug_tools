#!/usr/bin/env python3
import time
from pymavlink import mavutil

# 1) Connection parameters
connection_string = "udp:0.0.0.0:14550"

# 2) Open the MAVLink connection
mav = mavutil.mavlink_connection(connection_string)

# 3) Wait for the first heartbeat to ensure the link is live
print("Waiting for heartbeat...")
mav.wait_heartbeat()
print(f"Heartbeat received from System {mav.target_system}, Component {mav.target_component}")

# 4) Send a COMMAND_LONG to request ALL available modes
#
#    MAV_CMD_REQUEST_MESSAGE = 512
#    Param1 = message ID to request (435 = AVAILABLE_MODES)
#    Param2 = 0 to request all modes
#    Other params unused (set to 0)
mav.mav.command_long_send(
    mav.target_system,
    1,
    mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
    0,                              # confirmation
    435,
    0, 0, 0, 0, 0, 0                # params 2–7 unused
)

print("Sent request for all available modes (param2=0).")

# 5) Loop and collect AVAILABLE_MODES messages until we've seen them all
#
#    The first field in each AVAILABLE_MODES is 'number_modes', telling you
#    how many messages to expect in total.
modes = []
expected_count = None

print("Waiting for AVAILABLE_MODES messages...")
while True:
    # 4) recv_match with no type filter returns any incoming message
    msg = mav.recv_match(blocking=True, timeout=1)
    if msg:
        # print the full message (fields and values)
        print(msg)

# # 6) (Optional) Sort and display final list
# modes.sort(key=lambda x: x[0])
# print("\nFinal list of available modes:")
# for idx, name in modes:
#     print(f"  {idx:2d}: {name}")
