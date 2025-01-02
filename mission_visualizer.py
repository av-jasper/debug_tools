import argparse
from pymavlink import mavutil
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button


def get_command_name(command_id):
    """
    Maps a MAVLink command ID to its command name using pymavlink.
    """
    try:
        # Get the MAVLink command name
        command_name = mavutil.mavlink.enums['MAV_CMD'][command_id].name
        return command_name
    except KeyError:
        # Return a placeholder if the command ID is not found
        return f"Unknown Command ({command_id})"


def get_mission_count(mavlink_connection):
    """
    Requests the total number of mission items from the drone.
    """
    print("Requesting mission count...")
    
    # Send MISSION_REQUEST_LIST to get the mission count
    mavlink_connection.mav.mission_request_list_send(
        mavlink_connection.target_system, mavlink_connection.target_component
    )
    
    # Wait for MISSION_COUNT response
    while True:
        msg = mavlink_connection.recv_match(blocking=True, timeout=5)
        if not msg:
            print("Failed to receive mission count.")
            return 0
        if msg.get_type() == "MISSION_COUNT":
            print(f"Mission count received: {msg.count}")
            data = msg.to_dict()
            for key, value in data.items():
                print(f"{key}: {value}")
            return msg.count


def request_waypoint(mavlink_connection, waypoint_index):
    """
    Requests a specific waypoint from the drone.
    """
    
    # Send MISSION_REQUEST_INT for the specified waypoint index
    mavlink_connection.mav.mission_request_int_send(
        mavlink_connection.target_system,
        mavlink_connection.target_component,
        waypoint_index
    )

    # Wait for the response
    while True:
        msg = mavlink_connection.recv_match(blocking=True, timeout=5)
        if not msg:
            print(f"Failed to receive waypoint {waypoint_index}")
            return None
        if msg.get_type() == "MISSION_ITEM_INT":
            lat = msg.x / 1e7
            lon = msg.y / 1e7
            alt = msg.z
            seq = msg.seq
            command = msg.command
            frame = msg.frame
            command_name = get_command_name(command)
            param1 = msg.param1
            param2 = msg.param2
            param3 = msg.param3
            param4 = msg.param4

            return seq, lat, lon, alt, command_name, frame, param1, param2, param3, param4


from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def visualize_waypoints(waypoints):
    """
    Visualizes waypoints on a 3D map, including circles for non-zero param2 values.
    Adds sliders for Z-axis rotation and buttons for preset views.
    """
    # Create the figure and the 3D subplot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Determine global altitude reference if the first waypoint is in frame 0
    global_alt_reference = None
    if waypoints[0][5] == 0:  # frame=0
        global_alt_reference = waypoints[0][3]  # Altitude of the first waypoint

    # Initialize lists for the direction line
    lons, lats, alts = [], [], []

    for wp in waypoints:
        seq, lat, lon, alt, command_name, frame, param1, param2, param3, param4 = wp

        # Adjust altitude for relative frame (frame=3)
        if frame == 3 and global_alt_reference is not None:
            alt += global_alt_reference

        # Collect points for the direction line
        if lon != 0 or lat != 0:
            lons.append(lon)
            lats.append(lat)
            alts.append(alt)

        # Plot the waypoint as a point
        ax.scatter(lon, lat, alt, marker='o', color='blue', label=f"WP {seq}")
        ax.text(lon, lat, alt, f"{seq}", fontsize=8, color='black', ha='right', va='bottom')

        # Draw a circle if param2 (radius) is non-zero
        if param2 > 0:
            # Approximate the radius in degrees for the horizontal circle
            radius_deg = param2 / 111000  # Convert meters to degrees
            u = np.linspace(0, 2 * np.pi, 100)
            x_circle = lon + radius_deg * np.cos(u)
            y_circle = lat + radius_deg * np.sin(u)
            z_circle = np.full_like(x_circle, alt)  # Altitude stays constant for the circle
            ax.plot(x_circle, y_circle, z_circle, color='red', linestyle='--')
        elif param3 > 0:
            # Approximate the radius in degrees for the horizontal circle
            radius_deg = param3 / 111000  # Convert meters to degrees
            u = np.linspace(0, 2 * np.pi, 100)
            x_circle = lon + radius_deg * np.cos(u)
            y_circle = lat + radius_deg * np.sin(u)
            z_circle = np.full_like(x_circle, alt)  # Altitude stays constant for the circle
            ax.plot(x_circle, y_circle, z_circle, color='red', linestyle='--')

    # Add a direction line connecting all waypoints
    if lons and lats and alts:
        ax.plot(lons, lats, alts, color='green', linestyle='-', label='Direction Line')

        # Automatically adjust the view for better visualization
    all_lons = [wp[2] for wp in waypoints if wp[2] != 0]
    all_lats = [wp[1] for wp in waypoints if wp[1] != 0]
    all_alts = [wp[3] if wp[5] == 0 else wp[3] + global_alt_reference for wp in waypoints]

    if all_lons and all_lats:
        lon_min, lon_max = min(all_lons), max(all_lons)
        lat_min, lat_max = min(all_lats), max(all_lats)

        # Add padding to the limits to "zoom out"
        padding_lon = (lon_max - lon_min) * 0.4
        padding_lat = (lat_max - lat_min) * 0.4

        max_range = max(lon_max - lon_min, lat_max - lat_min) / 2
        mid_x = (lon_min + lon_max) / 2
        mid_y = (lat_min + lat_max) / 2

        # Set equal length for latitude and longitude
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)

    # Altitude axis remains independent
    if all_alts:
        alt_min, alt_max = min(all_alts), max(all_alts)
        padding_alt = (alt_max - alt_min) * 0.4
        ax.set_zlim(alt_min - padding_alt, alt_max + padding_alt)

    # Set labels and title
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Altitude (m)")
    ax.set_title("Mission Waypoints 3D Visualization")

    # Function to update the plot view
    def update_view(val):
        z_angle = slider_z.val  # Get the value from the Z-axis slider
        ax.view_init(elev=90, azim=z_angle)  # Update the view with fixed elevation

    # Button callback to set top-down view along Z-axis
    def view_top(event):
        ax.view_init(elev=90, azim=0)  # Top-down view
        fig.canvas.draw_idle()

    # Button callback to reset to default view
    def reset_view(event):
        ax.view_init(elev=30, azim=45)  # Default view
        fig.canvas.draw_idle()

    # Add slider for Z-axis rotation
    slider_ax = plt.axes([0.25, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
    slider_z = Slider(slider_ax, 'Z Rotation', 0, 360, valinit=0)
    slider_z.on_changed(update_view)

    # Add button for top-down Z-axis view
    button_ax_top = plt.axes([0.8, 0.85, 0.1, 0.05])
    button_top = Button(button_ax_top, 'Top View')
    button_top.on_clicked(view_top)

    # Add button to reset view
    button_ax_reset = plt.axes([0.8, 0.78, 0.1, 0.05])
    button_reset = Button(button_ax_reset, 'Reset View')
    button_reset.on_clicked(reset_view)

    # Show the plot
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Download all MAVLink waypoints sequentially.")
    parser.add_argument("--port", type=int, default=14551, help="UDP port for MAVLink connection.")
    args = parser.parse_args()

    # Establish MAVLink connection
    mavlink_connection = mavutil.mavlink_connection(f"udp:0.0.0.0:{args.port}")
    mavlink_connection.wait_heartbeat()
    print("Heartbeat received from the drone.")

    # Get the total number of mission items
    mission_count = get_mission_count(mavlink_connection)
    if mission_count == 0:
        print("No mission items to download.")
        return

    # Request each mission item sequentially and collect waypoints
    waypoints = []
    print("\nDownloading mission items:")
    for i in range(mission_count):
        waypoint = request_waypoint(mavlink_connection, i)
        if waypoint:
            waypoints.append(waypoint)
            print(
                f"  WP {waypoint[0]}: Lat={waypoint[1]}, Lon={waypoint[2]}, Alt={waypoint[3]} m, "
                f"Command={waypoint[4]}, Frame={waypoint[5]}, Param1={waypoint[6]}, Param2={waypoint[7]}, "
                f"Param3={waypoint[8]}, Param4={waypoint[9]}"
            )

    # Visualize waypoints
    visualize_waypoints(waypoints)


if __name__ == "__main__":
    main()
