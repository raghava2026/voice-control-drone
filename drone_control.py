from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# Connect to SITL (ArduPilot) on default port
print("Connecting to vehicle on 127.0.0.1:14550...")
vehicle = connect('127.0.0.1:14550', wait_ready=True)

def arm_and_takeoff(target_altitude):
    print("Arming motors...")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print(f"Taking off to {target_altitude} meters...")
    vehicle.simple_takeoff(target_altitude)

    while True:
        print(f"Altitude: {vehicle.location.global_relative_frame.alt:.2f}")
        if vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def land():
    print("Landing...")
    vehicle.mode = VehicleMode("LAND")

def rtl():
    print("Returning to launch...")
    vehicle.mode = VehicleMode("RTL")

def move_forward(distance):
    """
    Very basic movement: moves north by 'distance' meters
    """
    print(f"Moving forward {distance} meters...")
    current = vehicle.location.global_relative_frame
    target = LocationGlobalRelative(current.lat + (distance * 1e-5), current.lon, current.alt)
    vehicle.simple_goto(target)

def disarm():
    print("Disarming...")
    vehicle.armed = False