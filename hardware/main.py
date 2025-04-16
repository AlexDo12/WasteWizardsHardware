# import statements
from ultrasonic import Ultrasonic
from motor import servoMotor
import time
from pir import Pir


def dist():
    distance = 0
    return dist

def rotate():
    a = 0

def trapdoor():
    a = 0

def scanImg():
    classification = ""
    return classification

ULTRASONIC_ECHO_PIN = 23
ULTRASONIC_TRIGGER_PIN = 24

PIR_MOTION_PIN = 14

# TODO: What should these pins be
SPIN_MOTOR_PIN = 22
DOOR_MOTOR_PIN = 30

# used for averaging bin capacity
usonic_distances = []

if __name__ == "__main__":
        usonic = Ultrasonic(ULTRASONIC_ECHO_PIN, ULTRASONIC_TRIGGER_PIN, 1)
        pir = Pir(PIR_MOTION_PIN)

        conn = usonic.connect_db()
        usonic.setup()
        pir.setup()

        spin_motor = servoMotor(SPIN_MOTOR_PIN, 270)
        door_motor = servoMotor(DOOR_MOTOR_PIN, 180)

        while True:
            time.sleep(2)
            # detect motion (trash being placed) and wait for motion to stop (hand removed)
            pir.wait_for_motion()
            pir.wait_for_stop()
            time.sleep(1)

            print("Hand removed. Running sort logic")
            # Photo trash
            # Do AI stuff
            bin = 2

            # Rotate to bin
            spin_motor.set_angle(90 * bin)
                    
            # Open trapdoor
            door_motor.set_angle(180)
                    
            # Set ultrasonic bin & measure bin capacity
            usonic.bin = bin  # TODO: CHANGE THIS ACCORDINGLY
            usonic.update_fill_level(conn, usonic.getCapacity(usonic.run()))

            # Close trapdoor
            door_motor.set_angle(0)

            # Rotate backto original pos
            spin_motor.set_angle(0)
            time.sleep(1)


# wstwz step by step

# 1. detect when trash is inserted
# 2. scan the trash
# 3. rotate to bin
# 4. open trapdoor
# 5. Set ultrasonic bin & measure bin capacity
# 6. close trapdoor
# 7. rotate back to original position
# back to step 1
