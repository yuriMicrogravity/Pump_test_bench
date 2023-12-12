from ina219 import INA219
import time

SHUNT_OHMS = 0.1
#MAX_EXPECTED_AMPS = 0.4

def read_current_sensor():
    ina = INA219(SHUNT_OHMS)
    ina.configure(ina.RANGE_16V, ina.GAIN_AUTO)
    motor_current = ina.current()
    #print(f"Current = {motor_current:.3f} mA")
    return motor_current
    
    #print("Bus Voltage    : %.3f V" % ina.voltage())
    #print("Bus Current    : %.3f mA" % ina.current())
    #print("Supply Voltage : %.3f V" % ina.supply_voltage())
    #print("Shunt voltage  : %.3f mV" % ina.shunt_voltage())
    #print("Power          : %.3f mW" % ina.power())

#read_current_sensor()