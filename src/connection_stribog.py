#!/usr/bin/env python3
import time
from pymavlink import mavutil

# Connection string (adjust as needed)
CONNECTION_STRING = "udp:0.0.0.0:14550"
# CONNECTION_STRING = "udpout:192.168.55.1:46111"

def send_camera_capture_status_request():
    # 1) Open MAVLink connection
    mav = mavutil.mavlink_connection(CONNECTION_STRING)

    # 2) Wait for first heartbeat
    print("Waiting for heartbeat...")
    mav.wait_heartbeat()
    print(f"Heartbeat from system {mav.target_system}, component {mav.target_component}")

    # 3) Send MAV_CMD_REQUEST_CAMERA_CAPTURE_STATUS
    print("Sending MAV_CMD_REQUEST_CAMERA_CAPTURE_STATUS...")
    mav.mav.command_long_send(
        target_system=4,           # Use detected target system
        target_component=100,                      # Camera component ID (as per your capture)
        command=mavutil.mavlink.MAV_CMD_VIDEO_START_STREAMING,
        confirmation=0,
        param1=1,  # Request capture status
        param2=0,  # camera component id?? 
        param3=0,
        param4=0,
        param5=0,
        param6=0,
        param7=0
    )


    # 4) Wait for ACK
    print("Waiting for COMMAND_ACK...")
    ack = mav.recv_match(type='COMMAND_ACK', blocking=True, timeout=5)
    if ack:
        print(f"Received ACK: command={ack.command}, result={ack.result}")
    else:
        print("No ACK received within timeout.")

if __name__ == "__main__":
    try:
        send_camera_capture_status_request()
    except KeyboardInterrupt:
        print("Interrupted by user, exiting.")
