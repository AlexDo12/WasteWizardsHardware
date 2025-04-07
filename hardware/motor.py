import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class servoMotor:
    def __init__(self, servo_pin: int, maxAngle: float):
        self.servo_pin = servo_pin
        self.maxAngle = maxAngle
        self.angle = 0.0

        try:
            GPIO.setup(self.servo_pin, GPIO.OUT)
            self.pwm = GPIO.PWM(self.servo_pin, 50)
            self.pwm.start(0)
        except Exception as e:
            print(f"[ERROR] Failed to initialize PWM on pin {self.servo_pin}: {e}")
            self.pwm = None

    # Change the angle of the servo
    def set_angle(self, angle : float):
        # Verify pwm is initialized
        if self.pwm is None:
            print(f"[ERROR] PWM not initialized for pin {self.servo_pin}.")
            return

        try:
            self.angle = angle
            duty = self._angle_to_duty_cycle(self.angle)
            print(f"[Pin {self.servo_pin}] Moving to {angle}° → duty cycle {duty:.2f}%")
            self.pwm.ChangeDutyCycle(duty)
            time.sleep(1)
        except Exception as e:
            print(f"[ERROR] Failed to set angle on pin {self.servo_pin}: {e}")

    
    def _angle_to_duty_cycle(self, angle : float) -> float:
        # For most servos, 2.5% duty cycle is 0 degrees
        # and 12.5% duty cycle is max angle
        return 2.5 + (angle / self.maxAngle) * 10
    
    

    # Shouldn't really matter cause program will have closed when it needs to stop
    def stop(self):
        self.pwm.stop()
    
