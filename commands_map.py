from drone_control import arm_and_takeoff, land, rtl, move_forward, disarm

def handle_intent(intent, value=None):
    if intent == "TAKEOFF":
        arm_and_takeoff(value or 10)
    elif intent == "LAND":
        land()
    elif intent == "RTL":
        rtl()
    elif intent == "MOVE_FORWARD":
        move_forward(value or 5)
    elif intent == "DISARM":
        disarm()
    else:
        print(f"Unknown intent: {intent}")