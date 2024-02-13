from datetime import date, datetime
import time
import smbus
import csv
import RPi.GPIO as GPIO
from relay_updated import valve_set
from h_bridge import run_pump
from read_pressure_sensor_76 import read_psensor_amb
from read_pressure_sensor_77 import read_psensor_fluid
from as5600 import calculate_rpm, checkMagnet, calculate_avg_rpm
from sensors_check import check_sensors
#from current_sensor import read_current_sensor
from SHT35D_temp_humidity import *
from slf3s_1300f import measure_flow_rate, measure_flow_rate_average, signaling_flag_air, product_id_serial, flow_rate_live

test_config = input("Which configuration are you testing: ")
print(f"Test commencing for the configuration {test_config} on {date.today()}")
fnames = ['Test', 'Time', 'Local time', 'Direction', 'RPM', 'Current', 'Pressure', 'avg Flow']
with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
    writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
    writer.writeheader()

""" with open(f'/home/pi/Documents/test reports/{test_config}_summary.csv', mode='a') as summary_file:
    summary = ['summary']
    writer = csv.DictWriter(summary_file, fieldnames=summary, delimiter=',')
    writer.writeheader() """

def max_pressure_test_air_cw():
    # This function executes all steps required in the maximum pressure test for air in clockwise direction
    valve_set(1021314050)
    time.sleep(1)
    #Set the valve positions based on the setup
    run_pump("cw")
    #This function runs the pump in clockwise direction
    time.sleep(1)
    start_time = time.time()
    ambient_pressure = read_psensor_amb()
    local_time = 0
    time_limit = 20 # 2 minutes
    pressure_limit = 500 # 0.5 bar delta
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()

    try:
        while True:
            #Measure pressure
            fluid_pressure = read_psensor_fluid()
    	    # Ensure positive difference value for current_pressure
            current_pressure = abs(fluid_pressure - ambient_pressure)
            #motor_current = read_current_sensor()
            local_time = local_time + 0.5
            #This function reads value from the p ressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                run_pump("stop")
		        #summary: max_pressure_test_air_cw time limit reached with last pressure value ({current_pressure}) mbar. Test not successful.
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({local_time + 1}) seconds")
                run_pump("stop")
		        #summary: max_pressure_test_air_cw pressure limit reached within ({time.time()}) seconds. Test successful.
                break
            
            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")
            #print(f"Current = {motor_current:.3f} mA")
	        #Parameters to write in csv: test_id, time, current, pressure
            with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Test': '1', 'Time': datetime.now(), 'Local time': f'{local_time}', 'Direction': 'cw', 'RPM': 'cw', 'Current': 'NA', 'Pressure': f'{current_pressure:.2f}', 'avg Flow': 'NA'})

            """ with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                fnames = ['Time', 'Rotation', 'Current', 'Pressure']
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Time': datetime.now(), 'Rotation': 'cw', 'Current': f'{motor_current:.3f}', 'Pressure': current_pressure}) """

            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def min_vacuum_test_air_cw():
    # This function executes all steps required in the minimum vacuum test for air in clockwise direction
    valve_set(1020304150)
    #Set the valve positions based on the setup
    run_pump("cw")
    #This function runs the pump in clockwise direction
    time.sleep(1)
    start_time = time.time()
    local_time = 0
    ambient_pressure = read_psensor_amb()
    time_limit = 20 # 2 minutes
    pressure_limit = 500 # 0.5 bar delta
    
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()

    try:
        while True:
            #Measure pressure
            fluid_pressure = read_psensor_fluid()
    	    # Ensure positive difference value for current_pressure
            current_pressure = abs(fluid_pressure - ambient_pressure)
            #motor_current = read_current_sensor()
            local_time = local_time + 0.5
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure:.2f} mbar")

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure:.2f} mbar")
                run_pump("stop")                
		        #summary: min_vacuum_test_air_cw time limit reached with last pressure value ({current_pressure}) mbar. Test not successful.
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({local_time + 1}) seconds")
                run_pump("stop")                
		        #summary: min_vacuum_test_air_cw pressure limit reached within ({time.time()}) seconds. Test successful.
                break

            #Parameters to write in csv: test_id, time, current, pressure
            with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Test': '2', 'Time': datetime.now(), 'Local time': f'{local_time}', 'Direction': 'cw', 'RPM': 'cw', 'Current': 'NA', 'Pressure': f'{current_pressure:.2f}', 'avg Flow': 'NA'})

            """ with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                fnames = ['Time', 'Rotation', 'Current', 'Pressure']
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Time': datetime.now(), 'Rotation': 'cw', 'Current': f'{motor_current:.3f}', 'Pressure': current_pressure}) """

            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def air_release():
    # This function releases the air by creating atmospheric pressure before moving to ccw testings for air
    valve_set(1021314150)
    time.sleep(5)
    valve_set(1021304150)
    time.sleep(5)

def max_pressure_test_air_ccw():
    # This function executes all steps required in the maximum pressure test for air in counter-clockwise direction
    valve_set(1020304150)
    time.sleep(2)
    #Set the valve positions based on the setup
    run_pump("ccw")
    #This function runs the pump in counter-clockwise direction
    time.sleep(3)
    start_time = time.time()
    local_time = 0
    ambient_pressure = read_psensor_amb()
    time_limit = 20 # 20 seconds
    pressure_limit = 500 # 0.5 bar delta
    
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()
    
    try:
        while True:
            #Measure pressure
            fluid_pressure = read_psensor_fluid()
    	    # Ensure positive difference value for current_pressure
            current_pressure = abs(fluid_pressure - ambient_pressure)
            #motor_current = read_current_sensor()
            local_time = local_time + 0.5
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure:.2f} mbar")
                run_pump("stop")                
		        #summary: max_pressure_test_air_ccw time limit reached with last pressure value ({current_pressure}) mbar. Test not successful.
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({local_time + 1}) seconds")
                run_pump("stop")                
		        #summary: max_pressure_test_air_ccw pressure limit reached within ({time.time()}) seconds. Test successful.
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure:.2f} mbar")
	        #Parameters to write in csv: test_id, time, current, pressure
            #Parameters to write in csv: test_id, time, current, pressure
            with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Test': '3', 'Time': datetime.now(), 'Local time': f'{local_time}', 'Direction': 'ccw', 'RPM': 'ccw', 'Current': 'NA', 'Pressure': f'{current_pressure:.2f}', 'avg Flow': 'NA'})
            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def min_vacuum_test_air_ccw():
    # This function executes all steps required in the minimum vacuum test for air in counter-clockwise direction
    valve_set(1021314050)
    #Set the valve positions based on the setup
    time.sleep(1)
    run_pump("ccw")
    #This function runs the pump in counter-clockwise direction
    time.sleep(1)
    start_time = time.time()
    local_time = 0
    ambient_pressure = read_psensor_amb()
    time_limit = 20 # 20 seconds
    pressure_limit = 500 # 0.5 bar delta
    
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()
    
    try:
        while True:
            #Measure pressure
            fluid_pressure = read_psensor_fluid()
            #This function reads value from the pressure sensor inside the fluidic loop.
            current_pressure = abs(fluid_pressure - ambient_pressure)
            #motor_current = read_current_sensor()
            local_time = local_time + 0.5
            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                run_pump("stop")                
		        #summary: min_vacuum_test_air_cw time limit reached with last pressure value ({current_pressure}) mbar. Test not successful.
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({local_time + 1}) seconds")
                run_pump("stop")
		        #summary: min_vacuum_test_air_ccw pressure limit reached within ({time.time()}) seconds. Test successful.
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")
	        #Parameters to write in csv: test_id, time, current, pressure
            with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Test': '4', 'Time': datetime.now(), 'Local time': f'{local_time}', 'Direction': 'ccw', 'RPM': 'ccw', 'Current': 'NA', 'Pressure': f'{current_pressure:.2f}', 'avg Flow': 'NA'})

            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def filling_fluidic_loop():
    # This function fills the fluidic lines with distilled water to start with all water tests. 
    valve_set(1121314151)
    #Set the valve positions based on the setup to fill the fluidic loop with distilled water to start measuring flow rate of the pump
    run_pump("cw")
    #This function runs the pump in clockwise direction
    time.sleep(60)
    run_pump("stop")

def flow_rate_test_cw():
    #Valve configuration from previous test can be same. Just in case check for proper valve configuration
    valve_set(1121314151)
    average = 0.00
    avg_rpm = 0
    i = 0
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()
    for _ in range(3):
        run_pump("cw")
        #time.sleep(2)
        i = i +1
        flow = measure_flow_rate_average(50,60)
	    #Parameters to write in csv: test_id, time, rpm, current, flow
        average = average + flow
        rpm = calculate_avg_rpm()
        avg_rpm = avg_rpm + rpm
        with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Test': '5', 'Time': datetime.now(), 'Local time': 'NA', 'Direction': 'ccw', 'RPM': f'{rpm}', 'Current': 'NA', 'Pressure': 'NA', 'avg Flow': f'{average/i}'})
        run_pump("stop")
        time.sleep(3)
    avg_rpm = avg_rpm / 3
    average = average / 3
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Test': '5', 'Time': datetime.now(), 'Local time': 'NA', 'Direction': 'ccw', 'RPM': f'{avg_rpm}', 'Current': 'NA', 'Pressure': 'NA', 'avg Flow': f'{average}'})
    print(f"Average flow rate of the test in clockwise direction is {average:.3f} ml/min")
    #summary:(f"Average flow rate of the test in clockwise direction is {average:.3f} ml/min")

def max_pressure_test_water_cw():
    # This function executes all steps required in the maximum pressure test for water in clockwise direction
    valve_set(1121314051)
    time.sleep(2)
    #Set the valve positions based on the setup to measure maximum pressure built up by pump runing in clockwise direction
    run_pump("cw")
    #This function runs the pump in clockwise direction
    time.sleep(1)
    start_time = time.time()
    local_time = 0
    ambient_pressure = read_psensor_amb()
    time_limit = 20 # 20 seconds
    pressure_limit = 2200 # 2 bar delta
    
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()

    try:
        while True:
            #Measure pressure
            fluid_pressure = read_psensor_fluid()
    	    # Ensure positive difference value for current_pressure
            current_pressure = abs(fluid_pressure - ambient_pressure)
            local_time = local_time + 0.5
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                run_pump("stop")                
		        #summary: max_pressure_test_water_cw time limit reached with last pressure value ({current_pressure}) mbar. Test not successful.
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Last pressure measured {current_pressure} mbar")
                print(f"Time taken to reach the max pressure limit ({local_time + 1}) seconds")
                run_pump("stop")
		        #summary: max_pressure_test_water_cw pressure limit reached within ({time.time()}) seconds. Test successful.
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")
            with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Test': '6', 'Time': datetime.now(), 'Local time': f'{local_time}', 'Direction': 'ccw', 'RPM': 'ccw', 'Current': 'NA', 'Pressure': f'{current_pressure:.2f}', 'avg Flow': 'NA'})
            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def leak_test_cw():
    run_pump("stop")
    time.sleep(1)
    start_time = time.time()
    time_limit = 30 # 1 minute
    initial_pressure = read_psensor_fluid()
    
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()

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

""" def flow_rate_test_ccw_live():
    #Valve configuration to be set as the previous flow rate test.
    valve_set(1121314151)
    time.sleep(2)
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()
    i = 0
    average = 0.00
    global_average = 0.00
    if i <= 3:
        run_pump("ccw")
        time.sleep(2)
        local_average = 0.00
        i = i + 1
        for _ in range(60):
            #time.sleep(2)
            flow = flow_rate_live()
            average.append(flow)
            rpm = calculate_avg_rpm ()
            with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                    writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                    writer.writerow({'Test': '6', 'Time': datetime.now(), 'Local time': 'NA', 'Direction': 'ccw', 'RPM': f'{rpm}', 'Current': 'NA', 'Pressure': 'NA', 'avg Flow': f'{flow}'})
            run_pump("stop")
            time.sleep(3)
        local_average = sum(average) / len(average)
        print(f"Average flow rate of the cycle in counterclockwise direction is {local_average:.3f} ml/min")
    global_average = global_average + local_average
    global_average = global_average / 3
    print(f"Average flow rate of the test in counterclockwise direction is {global_average:.3f} ml/min")
        
    #summary:(f"Average flow rate of the test in clockwise direction is {average:.3f} ml/min") """

def flow_rate_test_ccw():
    #Valve configuration to be set as the previous flow rate test.
    valve_set(1121314151)
    run_pump("ccw")
    time.sleep(30)
    run_pump("stop")
    time.sleep(3)
    average = 0.00
    avg_rpm = 0
    i = 0
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()
    
    for _ in range(3):
        run_pump("ccw")
        i = i +1
        #time.sleep(2)
        flow = measure_flow_rate_average(50,60)
        average = average + flow
        rpm = calculate_avg_rpm ()
        avg_rpm = avg_rpm + rpm
        with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Test': '7', 'Time': datetime.now(), 'Local time': 'NA', 'Direction': 'ccw', 'RPM': f'{rpm}', 'Current': 'NA', 'Pressure': 'NA', 'avg Flow': f'{average/i}'})
        run_pump("stop")
        time.sleep(3)
    avg_rpm = avg_rpm / 3
    average = average / 3
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Test': '7', 'Time': datetime.now(), 'Local time': 'NA', 'Direction': 'ccw', 'RPM': f'{avg_rpm}', 'Current': 'NA', 'Pressure': 'NA', 'avg Flow': f'{average}'})
    print(f"Average flow rate of the test in clockwise direction is {average:.3f} ml/min")

    #summary:(f"Average flow rate of the test in clockwise direction is {average:.3f} ml/min")


def max_pressure_test_water_ccw():
    # This function executes all steps required in the maximum pressure test for water in counter-clockwise direction
    valve_set(1120304151)
    time.sleep(2)
    #Set the valve positions based on the setup to measure maximum pressure built up by pump runing in counter-clockwise direction
    run_pump("ccw")
    #This function runs the pump in counter-clockwise direction
    time.sleep(1)
    start_time = time.time()
    local_time = 0
    ambient_pressure = read_psensor_amb()
    time_limit = 20 # 20 seconds
    pressure_limit = 2200 # 2 bar delta
    
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()

    try:
        while True:
            #Measure pressure
            fluid_pressure = read_psensor_fluid()
    	    # Ensure positive difference value for current_pressure
            current_pressure = abs(fluid_pressure - ambient_pressure)
            local_time = local_time + 0.5
            #This function reads value from the pressure sensor inside the fluidic loop.

            #Checking if the duration limit is reached
            if time.time() - start_time >= time_limit:
                print("Time limit for this test reached. Stopping")
                print(f"Last pressure measured {current_pressure} mbar")
                run_pump("stop")
		        #summary: max_pressure_test_water_ccw time limit reached with last pressure value ({current_pressure}) mbar. Test not successful
                break

            #Checking if pressure in the fluidic loop is equal to or higher than the limit
            if current_pressure >= pressure_limit:
                print(f"Pressure reached the limit({pressure_limit}) successfully. Stopping.")
                print(f"Time taken to reach the max pressure limit ({local_time + 1}) seconds")
                run_pump("stop")
		        #summary: max_pressure_test_water_cw pressure limit reached within ({time.time()}) seconds. Test successful.
                break

            #Print or process the current pressure value
            print(f"Pressure:{current_pressure} mbar")
            with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writerow({'Test': '8', 'Time': datetime.now(), 'Local time': f'{local_time}', 'Direction': 'ccw', 'RPM': 'ccw', 'Current': 'NA', 'Pressure': f'{current_pressure:.2f}', 'avg Flow': 'NA'})
            #Adjust the sleep duration based on desired measurement frequency
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Measurement stopped due to user interruption")

def leak_test_ccw():
    run_pump("stop")
    time.sleep(1)
    start_time = time.time()
    time_limit = 20 # 1 minute
    initial_pressure = read_psensor_fluid()
    
    with open(f'/home/pi/Documents/test reports/{test_config}.csv', mode='a') as test_file:
                writer = csv.DictWriter(test_file, fieldnames=fnames, delimiter=',')
                writer.writeheader()

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
    valve_set(1121304150)
    run_pump("ccw")
    time.sleep(30)
    run_pump("stop")
    time.sleep(2)
    valve_set(1021314151)
    run_pump("cw")
    time.sleep(30)
    run_pump("stop")

def full_test_sequence():
    max_pressure_test_air_cw()
    time.sleep(1)
    air_release()
    time.sleep(1)
    min_vacuum_test_air_cw()
    time.sleep(1)
    air_release()
    time.sleep(1)
    max_pressure_test_air_ccw()
    time.sleep(1)
    air_release()
    time.sleep(3)
    min_vacuum_test_air_ccw()
    time.sleep(1)
    filling_fluidic_loop()
    time.sleep(1)
    flow_rate_test_cw()
    time.sleep(5)
    max_pressure_test_water_cw()
    time.sleep(1)
    valve_set(1121314151)
    time.sleep(3)
    #leak_test_cw()
    #time.sleep(1)
    flow_rate_test_ccw()
    time.sleep(5)
    max_pressure_test_water_ccw()
    time.sleep(1)
    valve_set(1121314151)
    time.sleep(3)
    #leak_test_ccw()
    #time.sleep(1)
    empty_fluidic_loop()
    time.sleep(1)
    print("Test sequence completed successfully")
    GPIO.cleanup()

def reset_testbench():
    run_pump("stop")
    valve_set(1121314151)
    time.sleep(3)
    valve_set(1020304050)
    time.sleep(3)
    GPIO.cleanup()

full_test_sequence()
""" reset_testbench()
time.sleep(5)
filling_fluidic_loop()
time.sleep(5) """
#check_sensors()
#checkMagnet()
#full_test_sequence()
#max_pressure_test_water_cw()
#leak_test_cw()
#reset_testbench()
#time.sleep(1)
""" valve_set(1121314151)
time.sleep(3)
min_vacuum_test_air_cw() """
