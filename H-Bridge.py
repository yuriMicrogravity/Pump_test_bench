import RPi.GPIO as GPIO
import time
HBridge1 = 5
HBridge2 = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(HBridge1, GPIO.OUT)
GPIO.setup(HBridge2, GPIO.OUT)
def run_pump(direction):
    if direction == "cw":
        GPIO.output(HBridge1, GPIO.HIGH)
        GPIO.output(HBridge2, GPIO.LOW)
        print("Pump is running in clockwise direction.")
    elif direction == "ccw":
        print("Pump is running in counterclockwise direction.")
        GPIO.output(HBridge1, GPIO.LOW)
        GPIO.output(HBridge2, GPIO.HIGH)
    elif direction == "stop":
        print("Pump is not running.")
        GPIO.output(HBridge1, GPIO.LOW)
        GPIO.output(HBridge2, GPIO.LOW)
    else:
        print("Invalid direction specified.")

run_pump("cw")
time.sleep(2)
run_pump("stop")
time.sleep(3)
run_pump("ccw")
time.sleep(2)
run_pump("stop")
time.sleep(3)
run_pump("ccw")
time.sleep(1)
run_pump("stop")
run_pump("cw")
time.sleep(2)
run_pump("stop")
GPIO.cleanup()