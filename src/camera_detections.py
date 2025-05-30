#!/usr/bin/env python3
import time
import math
from pymavlink import mavutil

# ——————————————————————————————————————————————
# Configuration
# ——————————————————————————————————————————————
# Adjust to your telemetry link (e.g. UDP endpoint, serial port, etc.)
CONNECTION_STRING    = "udpout:172.17.0.2:51956"

# The target system and component IDs.
# If known in advance, set here; otherwise, they will be filled in automatically.
TARGET_SYSTEM        = 0 
TARGET_COMPONENT     = 0 

# MAVLink message ID for CAMERA_TRACKING_IMAGE_STATUS
MSG_ID_TRACKING_STATUS = 275

# ——————————————————————————————————————————————
# Function to send a one-shot CAMERA_TRACKING_IMAGE_STATUS message
# ——————————————————————————————————————————————
def send_camera_tracking_status(
    tracking_status: int,
    tracking_mode: int,
    target_data: int,
    point_x: float = math.nan,
    point_y: float = math.nan,
    radius: float = math.nan,
    rec_top_x: float = math.nan,
    rec_top_y: float = math.nan,
    rec_bottom_x: float = math.nan,
    rec_bottom_y: float = math.nan,
    camera_device_id: int = 0
):
    """
    Send a one-shot CAMERA_TRACKING_IMAGE_STATUS (msg ID 275) message.

    Fields:
      tracking_status   (uint8): CAMERA_TRACKING_STATUS_FLAGS
      tracking_mode     (uint8): CAMERA_TRACKING_MODE
      target_data       (uint8): CAMERA_TRACKING_TARGET_DATA
      point_x, point_y  (float): Normalized coordinates (0..1) for point mode
      radius            (float): Normalized radius (0..1) for point mode
      rec_top_x, rec_top_y (float): Normalized top-left coordinates for rectangle mode
      rec_bottom_x, rec_bottom_y (float): Normalized bottom-right coords for rectangle mode
      camera_device_id  (uint8): Camera ID (0 for MAVLink camera)
    """
    # 1) Open MAVLink connection
    mav = mavutil.mavlink_connection(CONNECTION_STRING, autoreconnect=True)

    # 2) Wait briefly for connection to establish and heartbeat to be received
    mav.wait_heartbeat()
    sys_id = TARGET_SYSTEM or mav.target_system
    comp_id = TARGET_COMPONENT or mav.target_component
    print(f"Heartbeat from SYS {sys_id}, COMP {comp_id}")

    # 3) Send the CAMERA_TRACKING_IMAGE_STATUS message
    print(f"Sending CAMERA_TRACKING_IMAGE_STATUS (msg ID {MSG_ID_TRACKING_STATUS})...")
    mav.mav.camera_tracking_image_status_send(
        tracking_status,
        tracking_mode,
        target_data,
        point_x,
        point_y,
        radius,
        rec_top_x,
        rec_top_y,
        rec_bottom_x,
        rec_bottom_y,
        camera_device_id
    )
    print("Message sent.")

if __name__ == "__main__":
    # Example usage with default NaN for unknown fields
    try:
        send_camera_tracking_status(
            tracking_status=1,
            tracking_mode=2,
            target_data=0
            # point_x, point_y, etc. will default to NaN
        )
    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting.")
