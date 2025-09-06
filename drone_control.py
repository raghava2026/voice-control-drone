from dronekit import connect, VehicleMode
import time

vehicle = None   # not connected at start

def connect_drone(connection_string="127.0.0.1:5760"):
    global vehicle
    if vehicle is None:
        print(f"🔗 Connecting to drone at {connection_string} ...")
        vehicle = connect(connection_string, wait_ready=True)
        print("✅ Drone connected")
    return vehicle

def arm_and_takeoff(aTargetAltitude):
    v = connect_drone()
    print("🚁 Basic pre-arm checks")
    while not v.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("🚁 Arming motors")
    v.mode = VehicleMode("GUIDED")
    v.armed = True

    while not v.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("🚀 Taking off!")
    v.simple_takeoff(aTargetAltitude)

    while True:
        print(" Altitude:", v.location.global_relative_frame.alt)
        if v.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("✅ Reached target altitude")
            break
        time.sleep(1)

def execute_drone_command(intent):
    if intent == "TAKEOFF":
        arm_and_takeoff(10)
    elif intent == "LAND":
        v = connect_drone()
        print("🛬 Landing...")
        v.mode = VehicleMode("LAND")
    elif intent == "MOVE_FORWARD":
        print("➡️ Move forward (future implementation with velocity commands)")
    elif intent == "MOVE_BACKWARD":
        print("⬅️ Move backward (future implementation)")
    elif intent == "TURN_LEFT":
        print("↩️ Turn left (future implementation)")
    elif intent == "TURN_RIGHT":
        print("↪️ Turn right (future implementation)")
    elif intent == "UP":
        print("⬆️ Going up (future implementation)")
    elif intent == "DOWN":
        print("⬇️ Going down (future implementation)")
    elif intent == "STOP":
        print("⏹️ Stop (future implementation)")
    else:
        print("⚠️ Unknown intent")




if __name__ == "__main__":
    # Change to your SITL/QGC connection port
    connection_string = "tcp:127.0.0.1:5760"
    
    # Test the connection
    vehicle = connect_drone(connection_string)
    print("Connected to SITL drone ✅")

    # Example: Takeoff and land
    arm_and_takeoff(5)   # Take off to 5m
    time.sleep(5)        # Hover for a bit
    execute_drone_command("LAND")

    # Close vehicle
    vehicle.close()
    print("🚪 Connection closed.")
