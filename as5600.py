'''

Basic AS5600 readout

'''

import time, smbus, RPi.GPIO as GPIO

# Hardware constraints
I2C_BUS = 1
AS5600_I2C_ADDR = 0x36

# Configuration registers
# Refer to datasheet, page 19, for more details
# 0x07 - CONF - XX - WD - FTH(2:0) - SF(1:0)
# 0x08 - CONF - PWMF(1:0) - OUTS(1:0) - HYST(1:0) - PM(1:0)

# Output registers
# 0x0C / 0x0D - RAW_ANGLE(11:8) and RAW_ANGLE(7:0)
# 0x0E / 0x0F - ANGLE(11:8) and ANGLE(7:0)

# Status registers
# 0x0B - STATUS - MD(5), ML(4), MH(3)
# 0x1A - AGC - 8-bit
# 0x1B / 0x1C - MAGNITUDE(11:8) and MAGNITUDE(7:0)


AS5600_CONF_REG_ADDR = 0x07
AS5600_RAW_ANGLE_REG_ADDR = 0x0C 
AS5600_STATUS_REG_ADDR = 0x0B

#AS5600_CONF_BYTE1 = '1-100-001-1'
#AS5600_CONF_BYTE2 = '001-0-0-0-11'
AS5600_CONF_BYTE1 = 0b00000000
AS5600_CONF_BYTE2 = 0b00000001

# Auxiliary functions
def configureAS5600():
    BUS.write_byte_data(AS5600_I2C_ADDR, AS5600_CONF_REG_ADDR, AS5600_CONF_BYTE1)
    time.sleep(0.01)
    BUS.write_byte_data(AS5600_I2C_ADDR, AS5600_CONF_REG_ADDR+1, AS5600_CONF_BYTE2)
    time.sleep(0.01)
    
def readRawAngle():
    byte1 = BUS.read_byte_data(AS5600_I2C_ADDR, AS5600_RAW_ANGLE_REG_ADDR)
    byte2 = BUS.read_byte_data(AS5600_I2C_ADDR, AS5600_RAW_ANGLE_REG_ADDR+1)
    RawAngle = (byte1*256) + byte2
    print(str(RawAngle))
    #print(str(byte1*256 + byte2))
    
def checkMagnet():
    byte = BUS.read_byte_data(AS5600_I2C_ADDR, AS5600_STATUS_REG_ADDR)
    byte = byte & 0x38
    if  byte == 0x20:
        print("Magnet is detected")
        return True
    else:
        print("Magnet not detected")   
        return False

# Open I2C device
BUS = smbus.SMBus(I2C_BUS)
BUS.open(I2C_BUS) 

def calculate_rpm():
    # Variables for RPM calculation
    byte1 = BUS.read_byte_data(AS5600_I2C_ADDR, AS5600_RAW_ANGLE_REG_ADDR)
    byte2 = BUS.read_byte_data(AS5600_I2C_ADDR, AS5600_RAW_ANGLE_REG_ADDR+1)
    RawAngle1 = (byte1*256) + byte2
    previous_angle = RawAngle1* 0.087890625
    start_time = time.time()

    time.sleep(0.01)  # Adjust the sleep duration based on the expected RPM range

    byte1 = BUS.read_byte_data(AS5600_I2C_ADDR, AS5600_RAW_ANGLE_REG_ADDR)
    byte2 = BUS.read_byte_data(AS5600_I2C_ADDR, AS5600_RAW_ANGLE_REG_ADDR+1)
    RawAngle2 = (byte1*256) + byte2
    current_angle = RawAngle2 * 0.087890625

    # Quadrant 1
    if 0 <= current_angle <= 90:
        quadrant_number = 1

    # Quadrant 2
    elif 90 < current_angle <= 180:
        quadrant_number = 2

    # Quadrant 3
    elif 180 < current_angle <= 270:
        quadrant_number = 3

    # Quadrant 4
    else: 
        270 < current_angle < 360
        quadrant_number = 4

    # Measure time for one revolution
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # Calculate RPM
    cw = "Clockwise"
    ccw = "Counterclockwise"
    if  previous_angle < current_angle:
        angle_change = current_angle - previous_angle
        direction = cw
    else:
        direction = 2
        angle_change = previous_angle - current_angle
        direction = ccw

    rpm = (angle_change / 360) / elapsed_time * 60
    #return rpm
    print(f"RPM: {rpm:.2f}{direction}")

# Configure AS5600 operation
configureAS5600()
while True:
    print(f"direction: {direction}")
    calculate_rpm()
    time.sleep(0.2)
# Data acquisition
#checkMagnet()
#while True:
 #   if checkMagnet():
 #   readRawAngle()
 