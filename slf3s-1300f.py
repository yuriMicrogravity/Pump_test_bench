import argparse
import time
from sensirion_i2c_driver import LinuxI2cTransceiver, I2cConnection, CrcCalculator
from sensirion_driver_adapters.i2c_adapter.i2c_channel import I2cChannel
from sensirion_i2c_sf06_lf.device import Sf06LfDevice
from sensirion_i2c_sf06_lf.commands import (InvFlowScaleFactors)
from sensirion_driver_support_types.signals import AbstractSignal

parser = argparse.ArgumentParser()
parser.add_argument('--i2c-port', '-p', default='/dev/i2c-1')
args = parser.parse_args()

""" class SignalFlo(AbstractSignal):
    def __init__(self, raw_flow, inv_flow_scale_factor):
            self._flow = float(raw_flow)
            self._flow = self._flow / int(inv_flow_scale_factor)

        @property
        def value(self):
            return self._flow

        def __str__(self):
            return '{0:.2f}'.format(self.value)
 """
def product_id_serial():
    with LinuxI2cTransceiver(args.i2c_port) as i2c_transceiver:
        channel = I2cChannel(I2cConnection(i2c_transceiver),
                            slave_address=0x08,
                            crc=CrcCalculator(8, 0x31, 0xff, 0x0))
        sensor = Sf06LfDevice(channel)
        try:
            sensor.stop_continuous_measurement()
            time.sleep(0.1)
        except BaseException:
            ...
        (product_identifier, serial_number
        ) = sensor.read_product_identifier()
        print(f"product_identifier: {product_identifier}; "
            f"serial_number: {serial_number}; ")

def measure_flow_rate(sampling_frequency, measurement_duration):
    with LinuxI2cTransceiver(args.i2c_port) as i2c_transceiver:
        channel = I2cChannel(I2cConnection(i2c_transceiver),
                            slave_address=0x08,
                            crc=CrcCalculator(8, 0x31, 0xff, 0x0))
        sensor = Sf06LfDevice(channel)
        #sampling_frequency = 50
        sample_interval = 1 / sampling_frequency
        samples = []
        start_time = time.time()
        sensor.start_h2o_continuous_measurement()
        for i in range(500):
            try:
                time.sleep(sample_interval)
                (a_flow, a_temperature, a_signaling_flags
                ) = sensor.read_measurement_data(InvFlowScaleFactors.SLF3S_1300F)
                print(f"a_flow: {a_flow}; "
                    f"a_temperature: {a_temperature}; "
                    f"a_signaling_flags: {a_signaling_flags}; "
                    )
            except BaseException:
                continue
        sensor.stop_continuous_measurement()

def signaling_flag_air():
    i2c_transceiver = LinuxI2cTransceiver(args.i2c_port)
    channel = I2cChannel(I2cConnection(i2c_transceiver),
                        slave_address=0x08,
                        crc=CrcCalculator(8, 0x31, 0xff, 0x0))
    sensor = Sf06LfDevice(channel)
    sensor.start_h2o_continuous_measurement()
    time.sleep(0.02)
    (a_flow, a_temperature, a_signaling_flags) = sensor.read_measurement_data(InvFlowScaleFactors.SLF3S_1300F)
        
    if a_signaling_flags == 1 :
        print("Air bubble detected in the sensor")
    else:
        print("No air bubble in the sensor")
    sensor.stop_continuous_measurement()

product_id_serial()
#signaling_flag_air()
#measure_flow_rate()

def measure_flow_rate_average(sampling_frequency, measurement_duration):
    with LinuxI2cTransceiver(args.i2c_port) as i2c_transceiver:
        channel = I2cChannel(I2cConnection(i2c_transceiver),
                            slave_address=0x08,
                            crc=CrcCalculator(8, 0x31, 0xff, 0x0))
        sensor = Sf06LfDevice(channel)
        #sampling_frequency = 50
        sample_interval = 1 / sampling_frequency
        number_of_samples = (sampling_frequency) * (measurement_duration)
        global samples
        samples = 0.00
        start_time = time.time()
        sensor.start_h2o_continuous_measurement()
        try:
            while time.time() - start_time < measurement_duration:
                (a_flow, a_temperature, a_signaling_flags
                ) = sensor.read_measurement_data(InvFlowScaleFactors.SLF3S_1300F)
                def flow_rate(self, raw_flo):
                samples = samples + flow_rate
                print(f"a_flow: {a_flow}; "
                    f"a_temperature: {a_temperature}; "
                    f"a_signaling_flags: {a_signaling_flags}; "
                    )
                time.sleep(sample_interval)
        except KeyboardInterrupt:
            print("Measurement stopped due to user interruption")
        sensor.stop_continuous_measurement()
        #average_flow = samples / number_of_samples
        #print(f"Average flow of the measurement cycle is {average_flow} ml/min")
        """ average_flow = sum(samples) / len(samples)
        print(f"Average flow of the measurement cycle is {average_flow} ml/min")
        return average_flow """
    
measure_flow_rate_average(20,10)
#calculate_averag_flow()