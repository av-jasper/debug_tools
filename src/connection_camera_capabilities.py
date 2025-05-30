#!/usr/bin/env python3
import time
from pymavlink import mavutil

# ——————————————————————————————————————————————
# Configuration
# ——————————————————————————————————————————————
# Adjust to your telemetry link (e.g. UDP endpoint, serial port, etc.)
CONNECTION_STRING = "udpout:0.0.0.0:2600"

# The target system and component IDs.
# If you know them in advance, set here; otherwise,
# they will be filled in automatically from the first heartbeat.
TARGET_SYSTEM  = 0 
TARGET_COMPONENT = 0 

# The MAVLink message ID for CAMERA_INFORMATION
MSG_ID_CAMERA_INFORMATION = 259

# ——————————————————————————————————————————————
# Function to request a one‑shot CAMERA_INFORMATION message
# ——————————————————————————————————————————————
def request_camera_information():
    # 1) Open MAVLink connection
    mav = mavutil.mavlink_connection(CONNECTION_STRING, autoreconnect=True)
    
    # 2) Wait for a heartbeat to find system/component IDs
    # print("W aiting for heartbeat...")
    # mav.wait_heartbeat()
    sys_id = TARGET_SYSTEM 
    comp_id = TARGET_COMPONENT 
    print(f"Heartbeat received from system {sys_id}, component {comp_id}")
    
    # 3) Send MAV_CMD_REQUEST_MESSAGE (512) for message ID 259
    print(f"Requesting one‑shot CAMERA_INFORMATION (msg ID {MSG_ID_CAMERA_INFORMATION})…")
    mav.mav.command_long_send(
        target_system   = sys_id,
        target_component= comp_id,
        command         = mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
        confirmation    = 0,
        param1          = float(MSG_ID_CAMERA_INFORMATION),  # message ID to request
        param2          = 0,  # unused
        param3          = 0,  # unused
        param4          = 0,  # unused
        param5          = 0,  # unused
        param6          = 0,  # unused
        param7          = 0   # unused
    )
    
    # 4) Wait for the CAMERA_INFORMATION message
    print("Waiting for CAMERA_INFORMATION message…")
    message = mav.recv_match(type='CAMERA_INFORMATION', blocking=True, timeout=5)
    
    if message:
        # Print out the full message object
        print("Received CAMERA_INFORMATION:")
        print(message)
    else:
        print("Timeout: no CAMERA_INFORMATION received.")

if __name__ == "__main__":
    try:
        request_camera_information()
    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting.")
