from dronekit import connect, VehicleMode
import time

# Connect to the SITL on port 5760
print("Connecting to SITL...")
vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)

# Print some basic info
print("Connected to vehicle!")
print("GPS:", vehicle.gps_0)
print("Battery:", vehicle.battery)
print("Last Heartbeat:", vehicle.last_heartbeat)
print("Is Armable?", vehicle.is_armable)
print("Mode:", vehicle.mode.name)

# Try changing mode
print("Setting mode to GUIDED...")
vehicle.mode = VehicleMode("GUIDED")
time.sleep(2)
print("Mode now:", vehicle.mode.name)

vehicle.close()

