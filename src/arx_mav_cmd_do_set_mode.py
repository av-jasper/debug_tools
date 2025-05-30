
import sys
import struct
from pymavlink import mavutil

# Usage: python set_mode.py <custom_mode_u32>
# Example: python set_mode.py 10

def u32_to_float(u32_val):
    """
    Bit-cast a uint32 value into a float32.
    Returns a Python float that preserves the original 32-bit pattern.
    """
    # Pack uint32 into 4 bytes (little-endian), then unpack as float32
    packed = struct.pack('<I', u32_val)
    return struct.unpack('<f', packed)[0]


def main():
    # Validate and parse input
    if len(sys.argv) != 2:
        print("Usage: python set_mode.py <custom_mode_u32>")
        sys.exit(1)

    try:
        custom_mode_u32 = int(sys.argv[1])
    except ValueError:
        print("Error: custom_mode_u32 must be an integer.")
        sys.exit(1)

    if not (0 <= custom_mode_u32 <= 0xFFFFFFFF):
        print("Error: custom_mode_u32 must be between 0 and 2^32-1.")
        sys.exit(1)

    # Convert to float32 bit-pattern
    custom_mode_f32 = u32_to_float(custom_mode_u32)

    # 1) Open MAVLink connection
    mav = mavutil.mavlink_connection("udp:0.0.0.0:14550")
    print("Waiting for heartbeat...")
    mav.wait_heartbeat()
    print(f"Heartbeat received from system {mav.target_system}, component {mav.target_component}")

    # 2) Send DO_SET_MODE command with bit-cast param2
    mav.mav.command_long_send(
        mav.target_system,
        mav.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE,  # 176
        0,         # confirmation
        0,       # param1: MAV_MODE_FLAG_CUSTOM_MODE_ENABLED
        0,  # param2: custom mode bit-pattern
        0,       # param3: custom sub-mode (unused)
        0.0,       # param4 (unused)
        0.0,       # param5 (unused)
        0.0,       # param6 (unused)
        0.0        # param7 (unused)
    )
    print(f"DO_SET_MODE command sent with custom_mode_u32={custom_mode_u32} (as float bits).")

    while True:
        # 4) recv_match with no type filter returns any incoming message
        msg = mav.recv_match(blocking=True, timeout=1)
        if msg:
            # print the full message (fields and values)
            print(msg)


if __name__ == "__main__":
    main()
