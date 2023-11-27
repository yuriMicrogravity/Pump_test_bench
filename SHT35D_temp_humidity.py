#*****************************************************************************#
#													                            	
#		SHT3x - Sensirion Temperature Humidity sensor	      
#														                            
#		Simple script.									                   
#														                           
#		Olivier den Ouden								                    
#		Royal Netherlands Meterological Institute		        
#		RD Seismology and Acoustics						              
#		https://www.seabirdsound.org 					              
#														                            
#*****************************************************************************#

# Modules
import smbus
import time
import numpy as np

bus = smbus.SMBus(1)

# SHT3x hex adres
SHT3x_ADDR		= 0x44
SHT3x_SS		= 0x2C
SHT3x_HIGH		= 0x06
SHT3x_READ		= 0x00

def read_sht35d():
    while True:
        # MS to SL
        bus.write_i2c_block_data(SHT3x_ADDR,SHT3x_SS,[0x06])
        time.sleep(0.2)

        # Read out data
        data = bus.read_i2c_block_data(SHT3x_ADDR,SHT3x_READ,6)

        # Devide data into counts Temperature
        t_data = data[0] << 8 | data[1]

        # Devide data into counts Humidity
        h_data = data[3] << 8 | data[4]

        # Convert counts to Temperature/Humidity
        Humidity = 100.0*np.float(h_data)/65535.0
        Temperature = -45.0 + 175.0*np.float(t_data)/65535.0

        # Print Temperature and Humdity
        print(f"Temp:{Temperature:.2f}"+'  '+f"H:{Humidity:.2f}")
        time.sleep(1)
read_sht35d()
time.sleep(10)
