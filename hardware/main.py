# main.py
# WasteWizardHardware — added baseline comparison to reduce false positives

from ultrasonic import Ultrasonic
from motor import servoMotor
import time
from pir import Pir
# Recognition stuff
import openai
from picamera2 import Picamera2
import cv2, base64
import numpy as np
# Database upload
import psycopg2
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

load_dotenv()                    # looks for a .env file if it exists
try:
    openai.api_key = os.environ["OPENAI_API_KEY"]
except KeyError:
    raise RuntimeError(
        "OPENAI_API_KEY not set. Export it or put it in a .env file "
        "(never commit that file)."
    )

USERNAME = "ritchey"
TRASHCAN_ID = 1
ULTRASONIC_ECHO_PIN = 23
ULTRASONIC_TRIGGER_PIN = 24
PIR_MOTION_PIN = 14
SPIN_MOTOR_PIN = 18
DOOR_MOTOR_PIN = 27

# --- Baseline reference image -------------------------------------------------
BASELINE_IMAGE_PATH = "nothing.jpg"  # image of an empty drop-off surface
BASELINE_THRESHOLD = 0.02            # 2 % pixel-difference threshold

def _load_baseline():
    """Load and downscale the baseline reference image once at startup."""
    try:
        baseline_raw = cv2.imread(BASELINE_IMAGE_PATH)
        if baseline_raw is None:
            print(f"[Baseline] Warning: '{BASELINE_IMAGE_PATH}' not found; baseline filtering disabled.")
            return None
        return cv2.resize(baseline_raw, (640, 480), interpolation=cv2.INTER_AREA)
    except Exception as e:
        print(f"[Baseline] Error loading baseline image: {e}")
        return None

BASELINE_IMAGE = _load_baseline()

# ------------------------------------------------------------------------------
# used for averaging bin capacity
usonic_distances = []

def classify_trash(waste_types):
    """Capture an image, compare with baseline, and classify using GPT."""
    # 1) Configure camera for full-HD
    cam = Picamera2()
    cam.configure(cam.create_still_configuration(main={"size": (1920, 1080)}))
    try:
        cam.start()
        time.sleep(2)  # allow auto-exposure / AWB to settle

        # 2) Capture and downscale
        full_res = cam.capture_array()              # 1920×1080
        small = cv2.resize(full_res, (640, 480), interpolation=cv2.INTER_AREA)

        # ---- Baseline comparison ---------------------------------------------
        if BASELINE_IMAGE is not None:
            diff = cv2.absdiff(small, BASELINE_IMAGE)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            non_zero = cv2.countNonZero(gray)
            diff_ratio = non_zero / gray.size
            print(f"Baseline diff ratio: {diff_ratio:.4f}")
            # If the scene looks like the empty platform, skip GPT altogether
            if diff_ratio < BASELINE_THRESHOLD:
                print("Image similar to baseline — treating as 'no item'.")
                return "no item"
        # ----------------------------------------------------------------------

        cv2.imwrite("trash.jpg", small)           # saved in current dir
        # Base64 encode:
        _, buf = cv2.imencode('.jpg', small, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        b64 = base64.b64encode(buf).decode("utf-8")

        # 3) Build GPT prompt
        valid_waste_types_str = ", ".join(waste_types)
        system_prompt = (
            "You are a waste-sorting vision assistant.\n"
            "You will be shown an image captured above a trash drop-off platform.\n"
            "Classify the dominant object into exactly one of the following categories: " + valid_waste_types_str + ".\n"
            "If the object definitively does not belong to any category, respond with 'unknown'.\n"
            "If the platform is empty (bare wood) respond with 'null'.\n"
            "Respond with **only** the single word — no punctuation or additional text."
        )

        resp = openai.chat.completions.create(
            model="gpt-4o-mini",   # lighter / cheaper model
            messages=[
                {"role": "system",  "content": system_prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "Here is the image — what is on the platform?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]}
            ],
            max_tokens=10,
            temperature=0
        )

        full = resp.choices[0].message.content.strip().lower()
        print("Full GPT reply:", full)

        valid_responses = waste_types + ["unknown", "null"]
        return full if full in valid_responses else "trash"  # Default to trash if GPT returns something unexpected
    finally:
        cam.stop()
        cam.close()

def get_bin_config(conn, trashcan_id):
    """Get bin configuration and waste types from the database"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT bin_number, waste_type 
            FROM bin_config 
            WHERE trashcan = %s
        """, (trashcan_id,))
        bin_config = cur.fetchall()
    
    # Check if bin_config is empty
    if not bin_config:
        print("Warning: No bin configuration found! Using default configuration.")
        # Default configuration - bin 1: trash
        return {'trash': 1}, {1: 0}, ['trash'], 1
    
    # Create mapping from waste_type to bin_number
    waste_type_to_bin = {}
    bin_to_motor_index = {}  # Map database bin_number to motor index (0, 1, 2)
    waste_types = []
    
    # Process bin configuration
    for bin_number, waste_type in bin_config:
        waste_type_to_bin[waste_type] = bin_number
        waste_types.append(waste_type)
        bin_to_motor_index[bin_number] = bin_number - 1  # 0-based motor index
    
    # Find the trash bin for default
    trash_bin = waste_type_to_bin.get('trash')
    if trash_bin is None:
        trash_bin = bin_config[0][0]
    
    return waste_type_to_bin, bin_to_motor_index, waste_types, trash_bin

if __name__ == "__main__":
    usonic = Ultrasonic(ULTRASONIC_ECHO_PIN, ULTRASONIC_TRIGGER_PIN, 1)
    pir = Pir(PIR_MOTION_PIN)
    conn = usonic.connect_db()
    usonic.setup()
    pir.setup()
    spin_motor = servoMotor(SPIN_MOTOR_PIN, 270)
    door_motor = servoMotor(DOOR_MOTOR_PIN, 180)
    
    # Get bin configuration from database
    waste_type_to_bin, bin_to_motor_index, waste_types, trash_bin = get_bin_config(conn, TRASHCAN_ID)
    print(f"Configured waste types: {waste_types}")
    print(f"Default trash bin: {trash_bin}")
    
    # Set spin angle
    spin_motor.set_angle(135)
    
    # Close trapdoor
    door_motor.set_angle(68)
    
    while True:
        time.sleep(2)
        # detect motion (trash being placed) and wait for motion to stop (hand removed)
        pir.wait_for_motion()
        pir.wait_for_stop()
        time.sleep(0.5)
        print("Hand removed. Running sort logic")
        
        # Do AI stuff - pass waste types from bin_config
        classification = classify_trash(waste_types)
        print(f"Item classified as: {classification}")
        
        # Skip processing if no item detected
        if classification in ("no item", "null"):
            print("No item detected — skipping cycle.")
            continue
            
        # Determine which bin to use based on classification
        bin_number = trash_bin  # default
        if classification != "unknown" and classification in waste_type_to_bin:
            bin_number = waste_type_to_bin[classification]
        
        # Get the motor index (0-based) for this bin
        motor_index = bin_to_motor_index[bin_number]
        print(f"Using bin {bin_number} (motor position {motor_index})")
            
        # Upload what we just classified into the database
        try:
            with conn.cursor() as cur:
                # Grab the next ID
                cur.execute("""
                    SELECT COALESCE(MAX(id), 0) + 1
                    FROM waste_items
                """)
                next_id = cur.fetchone()[0]
            
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO waste_items (id, waste_type, bin_number, time, username, trashcan)
                    VALUES (%s,%s,%s,%s,%s,%s);
                    """,
                    (
                        next_id,
                        classification,
                        bin_number,
                        datetime.now(timezone.utc),
                        USERNAME,
                        TRASHCAN_ID
                    )
                )
            conn.commit()
            print("Logged item to waste_items.")
        except Exception as e:
            print(f"[DB-insert] Error logging item: {e}")
            
        # Rotate to bin - use the motor_index for angle calculation
        spin_angle = 135 * motor_index
        spin_motor.set_angle(spin_angle)
        
        # Open trapdoor
        door_motor.set_angle(180)
        
        # Set ultrasonic bin & measure bin capacity
        usonic.bin = bin_number
        usonic.update_fill_level(conn, usonic.getCapacity(usonic.run()))
        
        # Rotate back to original position
        spin_motor.set_angle(135)
        print("Back at original")
        
        # Close trapdoor
        door_motor.set_angle(68)
