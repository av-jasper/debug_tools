#!/usr/bin/env python3
import time
from pymavlink import mavutil

connection_string = "udp:0.0.0.0:14550"
forward_x = 200
loop_delay = 1.0

def main():
    # 1) Open the link
    mav = mavutil.mavlink_connection(connection_string)

    # 2) Wait for the first heartbeat and capture the returned message
    heartbeat = mav.wait_heartbeat()  # returns the HEARTBEAT message
    # Option A: read from the message directly
    print(f"Heartbeat from system={heartbeat}, component={heartbeat}")
    # Option B: or read the convenience fields on the connection
    print(f"Target system: {mav.target_system}, Target component: {mav.target_component}")

    try:
        # 3) Loop sending MANUAL_CONTROL
        while True:
            mav.mav.manual_control_send(
                mav.target_system,
                1,
                forward_x, 0, 0, 0, 0
            )
            print(f"Sent forward command x={forward_x}")
            time.sleep(loop_delay)

    except KeyboardInterrupt:
        # 4) On exit, send zeros to stop motion
        print("Interrupted—stopping vehicle.")
        mav.mav.manual_control_send(
            mav.target_system,
            mav.target_component,
            0, 0, 0, 0, 0
        )

if __name__ == "__main__":
    main()
