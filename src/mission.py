import asyncio
from dataclasses import astuple
from pymavlink import mavutil



class MAVLinkConnection:
    def __init__(self, host="localhost", port=14551, source_system=1, source_component=1):
        self.uri = f"udpin:{host}:{port}"
        self.source_system = source_system
        self.source_component = source_component
        self.master = mavutil.mavlink_connection(self.uri, source_system=source_system, source_component=source_component)

    async def wait_for_heartbeat(self):
        print("waiting for heartbeat")
        self.master.wait_heartbeat(blocking=True)
        print("received heartbeat")

    async def mavlink_listen_loop(self):
        while True:
            try:
                message = self.master.recv_match(blocking=False)
                if message:
                    await self.handle_messages(message)
                else:
                    await asyncio.sleep(0.001)
            except Exception as error:
                print(f"Error: {error}")
                break

    async def request_params_list(self):
        master = self.master.target_system
        target = self.master.target_component
        self.master.mav.param_request_list_send(
            target_system=self.master.target_system,
            target_component=self.master.target_component,
        )

    async def handle_messages(self, msg):
        if msg.get_type() in ("HEARTBEAT", "POSITION_TARGET_GLOBAL_INT", "BATTERY_STATUS", "PING", "OPEN_DRONE_ID_LOCATION", "ESTIMATOR_STATUS", "SCALED_PRESSURE","UTM_GLOBAL_POSITION", "VIBRATION", "SYSTEM_TIME", "HOME_POSITION","ALTITUDE","ATTITUDE_TARGET", "EXTENDED_SYS_STATE","POSITION_TARGET_LOCAL_NED", "VFR_HUD", "ATTITUDE","GPS_RAW_INT", "ODOMETRY", "GLOBAL_POSITION_INT","LOCAL_POSITION_NED","HIGHRES_IMU", "TIMESYNC","ATTITUDE_QUATERNION", "SYS_STATUS", "SERVO_OUTPUT_RAW"):
            return
        
        if msg.get_type() in ("WIND_COV", "NAV_CONTROLLER_OUTPUT"):
            return
        
        if msg.get_type() in ("UNKNOWN_8", "UNKNOWN_290", "UNKNOWN_291", "UNKNOWN_360", "UNKNOWN_380", "UNKNOWN_410", "UNKNOWN_411"):
            return
        
        if msg.get_type() in ("MISSION_CURRENT"):
            return
        
        print(f"SOURCE: {self.source_system} || {msg}")




async def main():

    connection = MAVLinkConnection(source_system=1)
    await connection.wait_for_heartbeat()
    mavlink_listener_task = asyncio.create_task(connection.mavlink_listen_loop())

    # vehicle_connection = MAVLinkConnection(source_system=255)
    # # await vehicle_connection.wait_for_heartbeat()
    # mavlink_vehicle_listener_task = asyncio.create_task(vehicle_connection.mavlink_listen_loop())

    # await asyncio.gather(mavlink_listener_task, mavlink_vehicle_listener_task)
    await asyncio.gather(mavlink_listener_task)


if __name__ == "__main__":
    asyncio.run(main())
