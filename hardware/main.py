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
ROTATE_MOTOR_PIN = 17
DOOR_MOTOR_PIN = 18

# used for averaging bin capacity
usonic_distances = []

if __name__ == "__main__":
    usonic = Ultrasonic(ULTRASONIC_ECHO_PIN, ULTRASONIC_TRIGGER_PIN, 1)
    pir = Pir(PIR_MOTION_PIN)
    try:
        conn = usonic.connect_db()
        usonic.setup()
        pir.setup()

        rotate_motor = servoMotor(ROTATE_MOTOR_PIN, 270)
        door_motor = servoMotor(DOOR_MOTOR_PIN, 180)

        # detect motion (trash being placed) and wait for motion to stop (hand removed)
        pir.wait_for_motion()
        pir.wait_for_stop()

        # Wait till motion is detected to open trapoor
        tolerance = 3
        starting_distance = usonic.run() # Probably better to hardcode this since someone could turn it on with hand in
        hand_removed_start = None
        handfree_time = time.time()
        countdown_required = 2 # seconds
        while True:
            measured_distance = usonic.run()
            print(f"Distance: {measured_distance:.2f} cm")

            # Once hand is in the way, wait for it to remove then start
            if (measured_distance < (starting_distance - tolerance)):
                print("Hand detected - waiting for removal")
                hand_removed_start = None
            else:
                if hand_removed_start is None:
                    hand_removed_start = time.time()
                elif time.time() - hand_removed_start >= countdown_required:
                    print("Hand removed for 2 seconds. Running sort logic")
                    # Photo trash
                    # Do AI stuff
                    bin = 1

                    # Rotate to bin
                    rotate_motor.set_angle(90 * bin)
                    
                    # Open trapdoor
                    door_motor.set_angle(180)
                    
                    # Set ultrasonic bin & measure bin capacity
                    usonic.bin = bin  # TODO: CHANGE THIS ACCORDINGLY
                    usonic.update_fill_level(conn, usonic.getCapacity(usonic.run()))

                    # Close trapdoor
                    door_motor.set_angle(0)

                    # Rotate backto original pos
                    rotate_motor.set_angle(0)

    except:
        print("Error in main")
    


# wstwz step by step

# 1. detect when trash is inserted
# 2. scan the trash
# 3. rotate to bin
# 4. open trapdoor
# 5. Set ultrasonic bin & measure bin capacity
# 6. close trapdoor
# 7. rotate back to original position
# back to step 1