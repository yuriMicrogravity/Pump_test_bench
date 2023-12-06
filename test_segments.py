import time
import smbus
import RPi.GPIO as GPIO
from relay_updated import valve_set
from h_bridge import run_pump
from read_pressure_sensor_76 import read_psensor_amb
from read_pressure_sensor_77 import read_psensor_fluid
from as5600 import calculate_rpm, checkMagnet
from sensors_check import check_sensors
from SHT35D_temp_humidity import read_sht35d
from slf3s_1300f import measure_flow_rate, measure_flow_rate_average, signaling_flag_air, product_id_serial

def max_pressure_test_air_cw():
    # This function executes all steps required in the maximum pressure test for air in clockwise direction
    valve_set(112130)
    #Set the valve positions based on the setup
    run_pump("cw")
    #This function runs the pump in clockwise direction
    start_time = time.time()
    time_limit = 120 # 2 minutes
    pressure_limit = 2000 # 2 bar absolute
    try:
        while True:
            #Measure pressure
            current_pressure = read_psensor_fluid()
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({time.time()}) seconds")
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")

            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def min_vacuum_test_air_cw():
    # This function executes all steps required in the minimum vacuum test for air in clockwise direction
    valve_set(112130)
    #Set the valve positions based on the setup
    run_pump("cw")
    #This function runs the pump in clockwise direction
    start_time = time.time()
    time_limit = 30 # 2 minutes
    pressure_limit = 300 # 2 bar absolute
    try:
        while True:
            #Measure pressure
            current_pressure = read_psensor_fluid()
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure <= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({time.time()}) seconds")
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")

            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def max_pressure_test_air_ccw():
    # This function executes all steps required in the maximum pressure test for air in counter-clockwise direction
    valve_set(112130)
    #Set the valve positions based on the setup
    run_pump("ccw")
    #This function runs the pump in counter-clockwise direction
    start_time = time.time()
    time_limit = 30 # 2 minutes
    pressure_limit = 2000 # 2 bar absolute
    try:
        while True:
            #Measure pressure
            current_pressure = read_psensor_fluid()
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({time.time()}) seconds")
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")

            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def min_vacuum_test_air_ccw():
    # This function executes all steps required in the minimum vacuum test for air in counter-clockwise direction
    valve_set(112130)
    #Set the valve positions based on the setup
    run_pump("ccw")
    #This function runs the pump in counter-clockwise direction
    start_time = time.time()
    time_limit = 30 # 2 minutes
    pressure_limit = 300 # 2 bar absolute
    try:
        while True:
            #Measure pressure
            current_pressure = read_psensor_fluid()
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure <= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({time.time()}) seconds")
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")

            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def filling_fluidic_loop():
    # This function executes all steps required in the maximum pressure test for air in counter-clockwise direction
    valve_set(112130)
    #Set the valve positions based on the setup to fill the fluidic loop with distilled water to start measuring flow rate of the pump
    run_pump("cw")
    #This function runs the pump in clockwise direction

def max_pressure_test_water_cw():
    # This function executes all steps required in the maximum pressure test for water in clockwise direction
    valve_set(112130)
    #Set the valve positions based on the setup to measure maximum pressure built up by pump runing in clockwise direction
    run_pump("cw")
    #This function runs the pump in clockwise direction
    start_time = time.time()
    time_limit = 120 # 2 minutes
    pressure_limit = 3000 # 3 bar absolute
    try:
        while True:
            #Measure pressure
            current_pressure = read_psensor_fluid()
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({time.time()}) seconds")
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")

            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def leak_test_cw():
    run_pump("stop")
    start_time = time.time()
    time_limit = 20 # 2 minutes
    initial_pressure = read_psensor_fluid()
    try:
        while True:
            #Measure pressure
            current_pressure = read_psensor_fluid()
            #This function reads value from the pressure sensor inside the fluidic loop.
            
            #Print or process the current pressure value
            print(f"Current Pressure is {current_pressure} mbar")
            
            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                pressure_diff = initial_pressure - current_pressure
                print(f"Pressure difference in {time_limit} seconds is {pressure_diff:.3f}")
                if pressure_diff >= 200 :
                    print("Pump is leaking in CW direction")
                else:
                    print("Pump is not leaking in CW direction")
                break
            
            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def max_pressure_test_water_ccw():
    # This function executes all steps required in the maximum pressure test for water in counter-clockwise direction
    valve_set(112130)
    #Set the valve positions based on the setup to measure maximum pressure built up by pump runing in counter-clockwise direction
    run_pump("ccw")
    #This function runs the pump in counter-clockwise direction
    start_time = time.time()
    time_limit = 120 # 2 minutes
    pressure_limit = 3000 # 3 bar absolute
    try:
        while True:
            #Measure pressure
            current_pressure = read_psensor_fluid()
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({time.time()}) seconds")
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")

            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def leak_test_ccw():
    run_pump("stop")
    start_time = time.time()
    time_limit = 20 # 2 minutes
    initial_pressure = read_psensor_fluid()
    try:
        while True:
            #Measure pressure
            current_pressure = read_psensor_fluid()
            #This function reads value from the pressure sensor inside the fluidic loop.
            
            #Print or process the current pressure value
            print(f"Current Pressure is {current_pressure} mbar")
            
            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                pressure_diff = initial_pressure - current_pressure
                print(f"Pressure difference in {time_limit} seconds is {pressure_diff:.3f}")
                if pressure_diff >= 200 :
                    print("Pump is leaking in CCW direction")
                else:
                    print("Pump is not leaking in CCW direction")
                break
            
            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

check_sensors()
checkMagnet()
#max_pressure_test_air_cw()
#leak_test_ccw()