import time
from as5600 import readRawAngle  # Assuming you have the readRawAngle function from as5600.py

def calculate_rpm():
    # Configure your AS5600 sensor and other setup if needed

    # Variables for RPM calculation
    previous_angle = readRawAngle()
    start_time = time.time()

    # Wait for at least one complete revolution
    time.sleep(0.05)  # Adjust the sleep duration based on the expected RPM range

    # Measure time for one revolution
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Calculate RPM
    current_angle = readRawAngle()
    angle_change = current_angle - previous_angle
    if angle_change < 0:
        angle_change += 4096  # Adjust for angle rollover

    rpm = (angle_change / 4096) / elapsed_time * 60
    dir = cw
    return rpm

# Test the function
if __name__ == "__main__":
    rpm_value = calculate_rpm()
    print(f"Current RPM: {rpm_value}+{dir}")

