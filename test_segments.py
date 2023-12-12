from datetime import date
import time
import smbus
import csv
import RPi.GPIO as GPIO
from relay_updated import valve_set
from h_bridge import run_pump
from read_pressure_sensor_76 import read_psensor_amb
from read_pressure_sensor_77 import read_psensor_fluid
from as5600 import calculate_rpm, checkMagnet
from sensors_check import check_sensors
from current_sensor import read_current_sensor
from SHT35D_temp_humidity import read_sht35d
from slf3s_1300f import measure_flow_rate, measure_flow_rate_average, signaling_flag_air, product_id_serial

test_config = input("Which configuration are you testing: ")
print(f"Test commencing for the configuration {test_config} on {date.today()}")


""" with open(f'{test_config}_{date.today}.csv', mode='w') as test_file:
    writer = csv.writer(test_file)
    header = ['Time', 'Rotation', 'Current', 'Pressure']
    writer.writerow(header) """

def max_pressure_test_air_cw():
    # This function executes all steps required in the maximum pressure test for air in clockwise direction
    valve_set(112130)
    #Set the valve positions based on the setup
    run_pump("cw")
    #This function runs the pump in clockwise direction
    start_time = time.time()
    time_limit = 10 # 2 minutes
    pressure_limit = 2000 # 2 bar absolute
    with open(f'{test_config}_{date.today}.csv', mode='w', newline='') as test_file:
        writer = csv.writer(test_file)
        header = ['Time', 'Rotation', 'Current', 'Pressure']
        writer.writerow(header)
    try:
        while True:
            #Measure pressure
            current_pressure = read_psensor_fluid()
            motor_current = read_current_sensor()
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                run_pump("stop")
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({time.time()}) seconds")
                run_pump("stop")
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")
            print(f"Current = {motor_current:.3f} mA")
            with open(f'{test_config}_{date.today}.csv', mode='w') as test_file:
                writer = csv.writer(test_file)
                line_write = [time.time(), 'cw', {motor_current}, {current_pressure}]
                writer.writerow(line_write)

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
    time_limit = 10 # 2 minutes
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
    time_limit = 10 # 2 minutes
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
    time_limit = 10 # 2 minutes
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
    # This function fills the fluidic lines with distilled water to start with all water tests. 
    valve_set(112130)
    #Set the valve positions based on the setup to fill the fluidic loop with distilled water to start measuring flow rate of the pump
    run_pump("cw")
    #This function runs the pump in clockwise direction
    time.sleep(10)
    run_pump("stop")

def flow_rate_test_cw():
    #Valve configuration from previous test can be same. Just in case check for proper valve configuration
    #valve_set()
    average = 0.00
    for _ in range(3):
        run_pump("cw")
        flow = measure_flow_rate_average(50,10)
        average = average + flow
        run_pump("stop")
        time.sleep(3)
    average = average / 3
    print(f"Average flow rate of the test in clockwise direction is {average} ml/min")

def max_pressure_test_water_cw():
    # This function executes all steps required in the maximum pressure test for water in clockwise direction
    valve_set(112130)
    #Set the valve positions based on the setup to measure maximum pressure built up by pump runing in clockwise direction
    run_pump("cw")
    #This function runs the pump in clockwise direction
    start_time = time.time()
    time_limit = 10 # 2 minutes
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
    time_limit = 10 # 2 minutes
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

def flow_rate_test_ccw():
    #Valve configuration to be set as the previous flow rate test.
    valve_set(112130)
    average = 0.00
    for _ in range(3):
        run_pump("ccw")
        flow = measure_flow_rate_average(50,10)
        average = average + flow
        run_pump("stop")
        time.sleep(3)
    average = average / 3
    print(f"Average flow rate of the test in clockwise direction is {average} ml/min")


def max_pressure_test_water_ccw():
    # This function executes all steps required in the maximum pressure test for water in counter-clockwise direction
    valve_set(112130)
    #Set the valve positions based on the setup to measure maximum pressure built up by pump runing in counter-clockwise direction
    run_pump("ccw")
    #This function runs the pump in counter-clockwise direction
    start_time = time.time()
    time_limit = 10 # 2 minutes
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
    time_limit = 10 # 2 minutes
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

def empty_fluidic_loop():
    #set valve in config that it fills with air and flushes out all water in the reservoir. 
    valve_set(102030)
    run_pump("cw")
    time.sleep(3)
    valve_set(112131)
    run_pump("ccw")
    time.sleep(3)
    run_pump("stop")



#check_sensors()
#valve_set(112131)
#time.sleep(3)
#valve_set(102030)
#checkMagnet()
#max_pressure_test_air_cw()
#leak_test_ccw()
#flow_rate_test_cw()

#Standard sequence for a full run of the testbench
checkMagnet()
check_sensors()
#test configuration name
max_pressure_test_air_cw()
min_vacuum_test_air_cw()
max_pressure_test_air_ccw()
min_vacuum_test_air_ccw()
filling_fluidic_loop()
flow_rate_test_cw()
max_pressure_test_water_cw()
leak_test_cw()
flow_rate_test_ccw()
max_pressure_test_water_ccw()
leak_test_ccw()
empty_fluidic_loop()
print("Test sequence completed successfully")
GPIO.cleanup()