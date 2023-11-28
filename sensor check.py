import time
import smbus
from as5600 import *

def detect_and_initialize_sensors():
    BUS = smbus.SMBus(1)
    i2c_addresses = {0x08, 0x36, 0x40, 0x44, 0x76, 0x77}
    counter = 0
    try:
        BUS.write_quick(0x08)
        print("Flow Sensor detected.")
        counter = counter+1

    except Exception as e:
        print("Flow Sensor not detected")

    try:
        BUS.write_quick(0x36)
        print("Encoder detected.")
        counter = counter+1

    except Exception as e:
        print("Encoder not detected")
    
    try:
        BUS.write_quick(0x40)
        print("Current Sensor detected.")
        counter = counter+1

    except Exception as e:
        print("Current Sensor not detected")

    try:
        BUS.write_quick(0x44)
        print("Temp. Sensor detected.")
        counter = counter+1

    except Exception as e:
        print("Temp. Sensor not detected")

    try:
        BUS.write_quick(0x76)
        print("Ambient Pressure Sensor detected.")
        counter = counter+1

    except Exception as e:
        print("Ambient Pressure Sensor not detected")

    try:
        BUS.write_quick(0x77)
        print("Fluid Pressure Sensor detected.")
        counter = counter+1

    except Exception as e:
        print("Fluid Pressure Sensor not detected")
    
    if counter == 6:
        print("Testbench ready")
    else:
        print("testbench not ready")

    BUS.close()

detect_and_initialize_sensors()
checkMagnet()