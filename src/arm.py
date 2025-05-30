#!/usr/bin/env python3
import time
from pymavlink import mavutil

# ——————————————————————————————————————————————
# Configuration
# ——————————————————————————————————————————————
# Adjust to your telemetry link (e.g. UDP endpoint, serial port, etc.)
CONNECTION_STRING = "udp:0.0.0.0:14550"  # Example UDP endpoint
# You can also use e.g. "tcp:hostname:port" or a serial port

# The target system and component IDs.
# If known in advance, set these; otherwise, they will be populated by heartbeat.
TARGET_SYSTEM    = 0
TARGET_COMPONENT = 0

# MAV_CMD for arming/disarming
CMD_ARM_DISARM = mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM

# ——————————————————————————————————————————————
# Function to arm or disarm the motors
# ——————————————————————————————————————————————
def set_arm_disarm(arm: bool):
    """
    Send a command to arm (True) or disarm (False) the vehicle motors.

    Parameters:
      arm (bool): True to arm, False to disarm.
    """
    # 1) Open MAVLink connection
    mav = mavutil.mavlink_connection(CONNECTION_STRING, autoreconnect=True)

    # 2) Wait for heartbeat
    print("Waiting for heartbeat...")
    mav.wait_heartbeat()
    sys_id = TARGET_SYSTEM or mav.target_system
    comp_id = TARGET_COMPONENT or mav.target_component
    print(f"Heartbeat from SYS {sys_id}, COMP {comp_id}")

    # 3) Send the arm/disarm command
    cmd_value = 1.0 if arm else 0.0
    action = "ARM" if arm else "DISARM"
    print(f"Sending {action} command to vehicle...")
    mav.mav.command_long_send(
        target_system=sys_id,
        target_component=comp_id,
        command=CMD_ARM_DISARM,
        confirmation=0,
        param1=cmd_value,  # 1 to arm, 0 to disarm
        param2=0,          # Must be 0
        param3=0,          # Unused
        param4=0,          # Unused
        param5=0,          # Unused
        param6=0,          # Unused
        param7=0           # Unused
    )

    # 4) Optionally, wait for ACK
    ack = mav.recv_match(type='COMMAND_ACK', blocking=True, timeout=5)
    if ack and ack.command == CMD_ARM_DISARM:
        result = mavutil.mavlink.enums['MAV_RESULT'][ack.result].description
        print(f"ACK received: {result}")
    else:
        print("No ACK received for arm/disarm command.")

if __name__ == "__main__":
    try:
        # Change to False to disarm
        set_arm_disarm(arm=True)
    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting.")
