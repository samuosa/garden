import smbus
import time

# I2C address of the ESP32
I2C_ADDRESS = 0x04

# Initialize I2C
bus = smbus.SMBus(1)  # Use '1' for I2C bus on the Raspberry Pi

def read_soil_sensors():
    # Read 4 bytes from ESP32
    data = bus.read_i2c_block_data(I2C_ADDRESS, 0, 4)
    
    # Combine high and low bytes for each sensor
    sensor1_value = (data[0] << 8) | data[1]

    
    return sensor1_value

while True:
    sensor1 = read_soil_sensors()
    print(f"Sensor 1 Moisture Level: {sensor1}")
    
    time.sleep(1)  # Wait for 1 second before reading again