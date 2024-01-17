import RPi.GPIO as GPIO
import time

# # Define the GPIO pins connected to the relay module
valve1 = 17 #Change to the actual GPIO pin number
valve2 = 27 #Change to the actual GPIO pin number
valve3 = 22 #Change to the actual GPIO pin number
valve4 = 10 #Change to the actual GPIO pin number
valve5 = 9 #Change to the actual GPIO pin number

# Define the valve number and state of the valves (0 for NO-Open, 1 for NC-Closed)
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
        print("Valve 1,2,3,4,5 are close.")
        GPIO.output(valve1, GPIO.LOW)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.LOW)
        GPIO.output(valve5, GPIO.LOW)
    elif num == 1020304151:
        # Max. pressure test air in cw direction
        print("Valve 1,2,3 are open and valve 4,5 are close.")
        GPIO.output(valve1, GPIO.HIGH)
        GPIO.output(valve2, GPIO.HIGH)
        GPIO.output(valve3, GPIO.HIGH)
        GPIO.output(valve4, GPIO.LOW)
        GPIO.output(valve5, GPIO.LOW)
    elif num == 1121304050:
        #Min. pressure(vacuum) test air in cw direction
        print("Valve 3,4,5 are open and valve 1,2 are close.")
        GPIO.output(valve1, GPIO.LOW)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.HIGH)
        GPIO.output(valve4, GPIO.HIGH)
        GPIO.output(valve5, GPIO.HIGH)
    elif num == 1021314050:
        #Max. pressure test air in ccw direction
        print("Valve 1,4,5 are open and valve 2,3 are close.")
        GPIO.output(valve1, GPIO.HIGH)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.HIGH)
        GPIO.output(valve5, GPIO.HIGH)
    elif num == 1120304151:
        # Min pressure(vacuum) test air in ccw direction 
        print("Valve 2,3 are open and valve 1,4,5 are close.")
        GPIO.output(valve1, GPIO.LOW)
        GPIO.output(valve2, GPIO.HIGH)
        GPIO.output(valve3, GPIO.HIGH)
        GPIO.output(valve4, GPIO.LOW)
        GPIO.output(valve5, GPIO.LOW)
    elif num == 1120314051:
        # For all fluidic line open (flowrate and filling for both directions)
        print("Valve 2,4 are open and valve 1,3,5 are close.")
        GPIO.output(valve1, GPIO.LOW)
        GPIO.output(valve2, GPIO.HIGH)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.HIGH)
        GPIO.output(valve5, GPIO.LOW)
    elif num == 1120304051:
        # For all fluidic line open (flowrate and filling for both directions)
        print("Valve 2,3,4 are open and valve 1,5 are close.")
        GPIO.output(valve1, GPIO.LOW)
        GPIO.output(valve2, GPIO.HIGH)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.HIGH)
        GPIO.output(valve5, GPIO.LOW)
    elif num == 1120314151:
        # Max. pressure and leak test water cw direction
        print("Valve 2 is open and valve 1,3,4,5 are close.")
        GPIO.output(valve1, GPIO.LOW)
        GPIO.output(valve2, GPIO.HIGH)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.LOW)
        GPIO.output(valve5, GPIO.LOW)
    elif num == 1021314051:
        # Max. pressure and leak test water ccw direction
        print("Valve 1,4 are open and valve 2,3,5 are close.")
        GPIO.output(valve1, GPIO.HIGH)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.HIGH)
        GPIO.output(valve5, GPIO.LOW)
    elif num == 1020314050:
        # Prepare for the next test fill with air
        print("Valve 1,2,4,5 are open and valve 3 is close.")
        GPIO.output(valve1, GPIO.HIGH)
        GPIO.output(valve2, GPIO.LOW)
        GPIO.output(valve3, GPIO.LOW)
        GPIO.output(valve4, GPIO.HIGH)
        GPIO.output(valve5, GPIO.LOW)        
    elif num == 1020304050:
        print("Valve 1,2,3,4,5 are open.")
        GPIO.output(valve1, GPIO.HIGH)
        GPIO.output(valve2, GPIO.HIGH)
        GPIO.output(valve3, GPIO.HIGH)
        GPIO.output(valve4, GPIO.HIGH)
        GPIO.output(valve5, GPIO.HIGH)
    else:
        print("Invalid valve setting specified.")
""" valve_set(102030)
time.sleep(3)
valve_set(112131)
time.sleep(3)
valve_set(112030)
time.sleep(3)
valve_set(102130)
time.sleep(3)
valve_set(102031)
time.sleep(3)
valve_set(112130)
time.sleep(3)
valve_set(102131)
time.sleep(3)
valve_set(102030)
time.sleep(3)
valve_set(112031)
time.sleep(3)
valve_set(112131)
time.sleep(3) """

""" GPIO.output(valve1, GPIO.HIGH)
print("Valve 1,2,3 are not open.")
time.sleep(15)
GPIO.output(valve1, GPIO.LOW)
print("Valve 1,2,3 are open.")
time.sleep(15)
GPIO.output(valve1, GPIO.HIGH)
time.sleep(3)
GPIO.output(valve1, GPIO.LOW)
time.sleep(3) """
#valve_set(102030)
#time.sleep(1)
#GPIO.cleanup()