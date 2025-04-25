# trapdoor_test.py
#
# Rotate the trapdoor servo from 0° to 180° and back to 0°.
# Make sure the 5 V rail and ground are connected properly
# before you run this!

import RPi.GPIO as GPIO
import time
from motor import servoMotor   # same import you’re already using

DOOR_MOTOR_PIN = 27            # GPIO pin your trapdoor servo is on
DOOR_SERVO_RANGE = 180         # max physical sweep of the servo in degrees

GPIO.setmode(GPIO.BCM)
GPIO.setup(DOOR_MOTOR_PIN, GPIO.IN)

def main() -> None:
    door = servoMotor(DOOR_MOTOR_PIN, DOOR_SERVO_RANGE)
    try:
        # Start at 0 °
        print("Moving to 0°")
        door.set_angle(68)
        time.sleep(1)          # pause so you can see the motion

        # Swing to 180 °
        print("Moving to 180°")
        door.set_angle(180)
        time.sleep(1)

        # Return to 0 °
        print("Returning to 0°")
        door.set_angle(68)
        time.sleep(1)

    finally:
        # If your servoMotor class exposes a cleanup() or stop() method,
        # call it here. Otherwise the GPIO library’s own cleanup
        # happens automatically when the program exits.
        pass


if __name__ == "__main__":
    main()
