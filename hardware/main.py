# import statements
from ultrasonic import Ultrasonic


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

# used for averaging bin capacity
usonic_distances = []

if __name__ == "__main__":
    usonic = Ultrasonic(ULTRASONIC_ECHO_PIN, ULTRASONIC_TRIGGER_PIN, 1)
    try:
        conn = usonic.connect_db()
        usonic.setup()

        # ... after trapdoor opens...MAKE SURE TO SET BIN NUMBER ON USONIC
        # report bin capacity
        usonic.bin = 1 # CHANGE THIS ACCORDINGLY
        usonic.update_fill_level(conn, usonic.run())
    except:
        print("Error in main")
    


# wstwz step by step

# 1. detect when trash is inserted
# 2. scan the trash
# 3. rotate to bin, set ultrasonic's bin to corresponding bin
# 4. open trapdoor
# 5. measure bin capacity
# 6. close trapdoor
# 7. rotate back to original position
# back to step 1