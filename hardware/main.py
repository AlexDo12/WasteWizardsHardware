# main.py
# WasteWizardHardware — same structure, camera teardown fix

from ultrasonic import Ultrasonic
from motor import servoMotor
import time
from pir import Pir

# Recognition stuff
import openai
from picamera2 import Picamera2
import cv2, base64

# TODO: CHANGE!! Directly embedding your key:
openai.api_key = "INSERT KEY"
ULTRASONIC_ECHO_PIN = 23
ULTRASONIC_TRIGGER_PIN = 24
PIR_MOTION_PIN = 14
SPIN_MOTOR_PIN = 18
DOOR_MOTOR_PIN = 27

# used for averaging bin capacity
usonic_distances = []

# GPT Wrapper to determine trash with proper teardown
def classify_trash():
    # 1) Configure camera for full‑HD
    cam = Picamera2()
    cam.configure(cam.create_still_configuration(main={"size": (1920, 1080)}))

    try:
        cam.start()
        time.sleep(2)  # allow auto‑exposure / AWB to settle

        # 2) Capture and downscale
        full_res = cam.capture_array()              # 1920×1080
        small = cv2.resize(
            full_res,
            (640, 480),                              # down to 640×480
            interpolation=cv2.INTER_AREA
        )
        cv2.imwrite("trash.jpg", small)           # saved in current dir

        # Base64 encode:
        _, buf = cv2.imencode('.jpg', small, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        b64 = base64.b64encode(buf).decode("utf-8")

        system_prompt = (
            "You will be shown an image. "
            "Classify it as exactly one of: trash, compost, recycle, no item, unknown. "
            "If unsure, reply 'unknown'. The background is a piece of wood; focus only on the platform. "
            "YOU MUST RESPOND WITH EXACTLY ONE OF THE 5 GIVEN RESPONSES (no punctuation)."
            "IF YOU DO NOT KNOW, SAY 'unknown'"
            "STOP RESPONDING WITH I DONT KNOW, SAY 'unknown'"
            "IF YOU ARE UNSURE AS TO WHAT THE ITEM IS, REPLY 'unknown' NOT A FULL SENTENCE"
            "All paper, metal, cardboard, and plastic itesm are considered recycle."
            "If the item is a wrapped item of food or a drink, it should be considered trash instead"
            "of recycle. This is because of contamination (even if its clearly unopened)"
            "Any kind of plant or leaves, food with no wrapping, etc should be considered compost"
        )

        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system",  "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "Here is the image—what is it?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]}
            ],
            max_tokens=100,
            temperature=0
        )

        full = resp.choices[0].message.content.strip().lower()
        print("Full GPT reply:", full)
        return full if full in {"trash", "compost", "recycle", "no item", "unknown"} else "trash"

    finally:
        # teardown camera session to free the resource
        cam.stop()
        cam.close()


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
        time.sleep(0.5)

        print("Hand removed. Running sort logic")
        # Do AI stuff
        classification = classify_trash()

        bin = 1  # default to trash
        if classification == "compost":
            bin = 0
        elif classification == "trash":
            bin = 1
        elif classification == "unknown":
            bin = 1
        elif classification == "recycle":
            bin = 2
        elif classification == "no item":
            continue

        # Rotate to bin
        spin_motor.set_angle(135 * bin)
        # Open trapdoor
        door_motor.set_angle(0)

        # Set ultrasonic bin & measure bin capacity
        usonic.bin = bin
        usonic.update_fill_level(conn, usonic.getCapacity(usonic.run()))

        # Close trapdoor
        door_motor.set_angle(180)

        # Rotate back to original pos
        spin_motor.set_angle(135)

# wstwz step by step
# 1. detect when trash is inserted
# 2. scan the trash
# 3. rotate to bin
# 4. open trapdoor
# 5. Set ultrasonic bin & measure bin capacity
# 6. close trapdoor
# 7. rotate back to original position
# back to step 1
