#!/usr/bin/env python3
import time
from pymavlink import mavutil

# Connection string (adjust as needed)
CONNECTION_STRING = "udp:0.0.0.0:14550"

def arm_drone():
    # 1) Open MAVLink connection
    mav = mavutil.mavlink_connection(CONNECTION_STRING)

    # 2) Wait for first heartbeat
    print("Waiting for heartbeat...")
    mav.wait_heartbeat()
    print(f"Heartbeat from system {mav.target_system}, component {mav.target_component}")

    # 3) Send ARM command:
    #    MAV_CMD_COMPONENT_ARM_DISARM = 400
    #    param1 = 1 to arm, 0 to disarm
    print("Sending ARM command...")
    mav.mav.command_long_send(
        mav.target_system,
        1,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0,      # confirmation
        0,      # param1: 1 to arm
        0, 0, 0, 0, 0, 0  # param2–7 unused
    )

    # 4) Wait for ACK
    print("Awaiting COMMAND_ACK...")
    ack = mav.recv_match(type='COMMAND_ACK', blocking=True, timeout=5)
    if not ack:
        print("No ACK received within timeout.")
        return

    # 5) Check the result
    if ack.command == mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM:
        result = ack.result
        if result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
            print("Arming successful!")
        else:
            print(f"Arming failed, ACK result: {result}")
    else:
        print(f"Received ACK for unexpected command: {ack.command}")

if __name__ == "__main__":
    try:
        arm_drone()
    except KeyboardInterrupt:
        print("Interrupted by user, exiting.")
