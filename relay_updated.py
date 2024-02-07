import RPi.GPIO as GPIO
import time

# # Define the GPIO pins connected to the relay module
valve1 = 17 #Change to the actual GPIO pin number
valve2 = 27 #Change to the actual GPIO pin number
valve3 = 22 #Change to the actual GPIO pin number
valve4 = 10 #Change to the actual GPIO pin number
valve5 = 9 #Change to the actual GPIO pin number

# Define the valve number and state of the valves (0 for not active, 1 for active, valves are NC type so not active means valve closed and no power supply)
def valve_set(num):
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Initialize the GPIO pins
    GPIO.setup(valve1, GPIO.OUT)
    GPIO.setup(valve2, GPIO.OUT)
    GPIO.setup(valve3, GPIO.OUT)
    GPIO.setup(valve4, GPIO.OUT)
    GPIO.setup(valve5, GPIO.OUT)
    #num = str(num)
    #state = str(state)
    if num == 1121314151:
        # Configuration for Flow-rate test and filling the fluidic loop with water
        print("Valve 1,2,3,4,5 are active.")
        GPIO.output(valve1, GPIO.LOW)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.LOW)
        GPIO.output(valve5, GPIO.LOW)
    elif num == 1021314050:
        # Configuartion for max. pressure test air in cw direction min pressure(vacuum) test air in ccw direction 
        print("Valve 1,4,5 are not active and valve 2,3 are active.")
        GPIO.output(valve1, GPIO.HIGH)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.HIGH)
        GPIO.output(valve5, GPIO.HIGH)
    elif num == 1020304150:
        # Configuartion for min. pressure(vacuum) test air in cw direction & max. pressure test air in ccw direction
        print("Valve 1,2,3,5 are not active and valve 4 is active.")
        GPIO.output(valve1, GPIO.HIGH)
        GPIO.output(valve2, GPIO.HIGH)
        GPIO.output(valve3, GPIO.HIGH)
        GPIO.output(valve4, GPIO.LOW)
        GPIO.output(valve5, GPIO.HIGH)
    elif num == 1021304150:
        # Configuartion for air flush between cw-ccw air tests
        print("Valve 1,3,5 are not active and valve 2,4 are active.")
        GPIO.output(valve1, GPIO.HIGH)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.HIGH)
        GPIO.output(valve4, GPIO.LOW)
        GPIO.output(valve5, GPIO.HIGH)
    elif num == 1121314051:
        # Configuartion for max pressure test water in cw direction 
        print("Valve 4 is not active and valve 1,2,3,5 are active.")
        GPIO.output(valve1, GPIO.LOW)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.HIGH)
        GPIO.output(valve5, GPIO.LOW)
    elif num == 1120304151:
        # Configuartion for max pressure test water in ccw direction
        print("Valve 2,3 are not active and valve 1,4,5 are active.")
        GPIO.output(valve1, GPIO.LOW)
        GPIO.output(valve2, GPIO.HIGH)
        GPIO.output(valve3, GPIO.HIGH)
        GPIO.output(valve4, GPIO.LOW)
        GPIO.output(valve5, GPIO.LOW)
    elif num == 1121304150:
        # Configuartion for flushing water with pump running in ccw direction
        print("Valve 3,5 are not active and valve 1,2,4 are active.")
        GPIO.output(valve1, GPIO.LOW)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.HIGH)
        GPIO.output(valve4, GPIO.LOW)
        GPIO.output(valve5, GPIO.HIGH)
    elif num == 1021314151:
        # Configuartion for flushing water with pump running in cw direction
        print("Valve 1 is not active and valve 2,3,4,5 are active.")
        GPIO.output(valve1, GPIO.HIGH)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.LOW)
        GPIO.output(valve5, GPIO.LOW)     
    elif num == 1020304050:
        print("Valve 1,2,3,4,5 are not active.")
        GPIO.output(valve1, GPIO.HIGH)
        GPIO.output(valve2, GPIO.HIGH)
        GPIO.output(valve3, GPIO.HIGH)
        GPIO.output(valve4, GPIO.HIGH)
        GPIO.output(valve5, GPIO.HIGH)
    else:
        print("Invalid valve setting specified.")
""" valve_set(1021314050)
time.sleep(3)
valve_set(1020304150)
time.sleep(3)
valve_set(1021304150)
time.sleep(3)
valve_set(1121314151)
time.sleep(3)
valve_set(1121314051)
time.sleep(3)
valve_set(1120304151)
time.sleep(3)
valve_set(1121304150)
time.sleep(3)
valve_set(1021314151)
time.sleep(3)
valve_set(1020304050)
time.sleep(3)
valve_set(1121314150)
time.sleep(3)
valve_set(1020304050)
time.sleep(3)
valve_set(1121314151)
time.sleep(3)
GPIO.cleanup() """