import RPi.GPIO as GPIO

class Pir:
    def __init__(self, motion_pin: int):
        self.motion_pin = motion_pin

    def setup(self):
        GPIO.setmode('BCM')
        GPIO.setup(self.motion_pin, GPIO.IN)

    def wait_for_motion(self):
        while GPIO.input(self.motion_pin, False):
            continue
        return
    
    def wait_for_stop(self):
        while GPIO.input(self.motion_pin, True):
            continue
        return