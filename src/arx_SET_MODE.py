#!/usr/bin/env python3
import time
import sys
from pymavlink import mavutil

# Connection string (adjust as needed)
CONNECTION_STRING = "udp:0.0.0.0:14550"

def set_mode(custom_mode: int, base_mode: int):
    """
    Send a MAVLink SET_MODE message.

    :param custom_mode: uint32 custom mode value (e.g. 10 for mission mode)
    :param base_mode:   uint8 base mode bitmask 
                        (e.g. mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED)
    """
    # 1) Open MAVLink connection
    mav = mavutil.mavlink_connection(CONNECTION_STRING)

    # 2) Wait for first heartbeat
    print("Waiting for heartbeat...")
    mav.wait_heartbeat()
    print(f"Heartbeat received from SYS {mav.target_system}, COMP {mav.target_component}")

    # 3) Send SET_MODE (msg 11)
    #
    #    Fields are (target_system, base_mode, custom_mode)
    mav.mav.set_mode_send(
        mav.target_system,
        base_mode,
        custom_mode
    )
    print(f"SET_MODE sent → base_mode={base_mode}, custom_mode={custom_mode}")

    # 4) (Optional) Wait for the vehicle to report the new mode in a heartbeat
    print("Waiting for mode-confirming heartbeat...")
    start = time.time()
    while True:
        # 4) recv_match with no type filter returns any incoming message
        msg = mav.recv_match(blocking=True, timeout=1)
        if msg:
            # print the full message (fields and values)
            print(msg)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python set_mode.py <custom_mode> <base_mode>")
        sys.exit(1)

    try:
        cm = int(sys.argv[1], 10)
        bm = int(sys.argv[2], 10)
    except ValueError:
        print("Both custom_mode and base_mode must be integers.")
        sys.exit(1)

    try:
        set_mode(custom_mode=cm, base_mode=bm)
    except KeyboardInterrupt:
        print("Interrupted by user, exiting.")
