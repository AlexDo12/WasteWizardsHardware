# Libraries
import RPi.GPIO as GPIO
import time
import psycopg2  # <-- Make sure this is included

class Ultrasonic:
    distances = []
    def __init__(self, echo_pin: int, trigger_pin: int, bin: int):
        self.echo_pin = echo_pin
        self.trigger_pin = trigger_pin
        self.bin = 1

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    # Connect to our NeonDB database
    def connect_db():
        # NeonDB PostgreSQL connection details
        DB_NAME = "neondb"
        DB_USER = "neondb_owner"
        DB_PASSWORD = "npg_rV3GK0DgSHNQ"
        DB_HOST = "ep-dry-mouse-a5h6zwqn-pooler.us-east-2.aws.neon.tech"
        DB_PORT = "5432"
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            print("Connected to the database successfully!")
            return conn
        except Exception as e:
            print(f"Database connection error: {e}")
            return None

    def update_fill_level(self, conn, fill_level):
        """Updates the fill level for bin_number = 1 in bin_config table."""
        try:
            cur = conn.cursor()
            fill_level_rounded = round(fill_level, 2)
            update_query = """
            UPDATE bin_config
            SET fill_level = %s
            WHERE bin_number = %s;
            """
            cur.execute(update_query, (fill_level_rounded, self.bin))
            conn.commit()
            cur.close()
            print(f"Updated bin fill level to {fill_level_rounded:.2f}")
        except Exception as e:
            print(f"Error updating fill level: {e}")

    def _distance(self):
        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        StartTime = time.time()
        StopTime = time.time()

        while GPIO.input(self.echo_pin) == 0:
            StartTime = time.time()

        while GPIO.input(self.echo_pin) == 1:
            StopTime = time.time()

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        return distance

    def run(self):
        for i in range(10):
            self.distances[i] = self._distance()
        return sum(self.distances)/len(self.distances)
        

if __name__ == '__main__':
    conn = connect_db()
    setupUsonic()
    try:
        while True:
            dist = distance()
            capacity = 1 - (dist - 38) / 56
            capacity = max(0.0, min(1.0, capacity))  # Clamp to [0,1]
            print(f"Bin Capacity: {(capacity*100):.1f}%")
            if dist < 20:
                print("Bin full!")

            if conn:
                update_fill_level(conn, capacity)

            time.sleep(4)
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        if conn:
            conn.close()
