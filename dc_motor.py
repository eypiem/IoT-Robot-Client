from enum import Enum
#import RPi.GPIO as GPIO


class MotorDir(Enum):
    CW = True
    CCW = False


class DCMotor:
    GPIO = None
    in_1 = None
    in_2 = None
    en = None
    pwm = None
    setup = False

    def __init__(self, GPIO, in_1, in_2, en):
        self.GPIO = GPIO
        self.in_1 = in_1
        self.in_2 = in_2
        self.en = en

    def setup_pins(self):
        self.GPIO.setup(self.in_1, self.GPIO.OUT)
        self.GPIO.setup(self.in_2, self.GPIO.OUT)
        self.GPIO.setup(self.en, self.GPIO.OUT)
        self.pwm = self.GPIO.PWM(self.en, 1000)
        self.pwm.start(0)
        self.setup = True

    def run(self, dir, spd):
        self.check_setup()
        if dir:
            self.GPIO.output(self.in_1, self.GPIO.HIGH)
            self.GPIO.output(self.in_2, self.GPIO.LOW)
            self.pwm.ChangeDutyCycle(spd)

    def stop(self):
        self.check_setup()
        self.GPIO.output(self.in_1, self.GPIO.LOW)
        self.GPIO.output(self.in_2, self.GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

    def check_setup(self):
        if not self.setup:
            raise Exception('DCMotor Exception', 'Run DCMotor().setup_pins first.')
