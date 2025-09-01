from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
from pymavlink import mavutil

# ------------------ HELPER FUNCTIONS ------------------

def send_ned_velocity(vehicle, velocity_x, velocity_y, velocity_z, duration):
    """
    Move vehicle in direction based on NED frame.
    velocity_x: m/s (forward +, back -)
    velocity_y: m/s (right +, left -)
    velocity_z: m/s (down +, up -)
    """
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED,  # frame
        0b0000111111000111,  # type mask (only velocities enabled)
        0, 0, 0,  # position
        velocity_x, velocity_y, velocity_z,  # m/s
        0, 0, 0,  # accelerations
        0, 0)     # yaw, yaw_rate

    for _ in range(0, duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)


def arm_and_takeoff(vehicle, target_altitude):
    print("Basic pre-arm checks...")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(target_altitude)

    while True:
        alt = vehicle.location.global_relative_frame.alt
        print(" Altitude:", alt)
        if alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# ------------------ MAIN SCRIPT ------------------

def main():
    print("Connecting to SITL...")
    vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)

    arm_and_takeoff(vehicle, 10)

    print("Moving forward...")
    send_ned_velocity(vehicle, 2, 0, 0, 3)   # forward 2 m/s for 3 sec

    print("Moving right...")
    send_ned_velocity(vehicle, 0, 2, 0, 3)   # right 2 m/s for 3 sec

    print("Moving backward...")
    send_ned_velocity(vehicle, -2, 0, 0, 3)  # backward 2 m/s for 3 sec

    print("Moving left...")
    send_ned_velocity(vehicle, 0, -2, 0, 3)  # left 2 m/s for 3 sec

    print("Landing...")
    vehicle.mode = VehicleMode("LAND")
    time.sleep(5)

    vehicle.close()
    print("Mission completed")

if __name__ == "__main__":
    main()

