import smbus
import time

# Set up the I2C bus
bus = smbus.SMBus(1)  # I2C bus on Raspberry Pi is usually 1
ESP32_I2C_ADDRESS = 0x04  # Address of the ESP32 as a slave

def read_soil_moisture():
    try:
        # Request one byte from the ESP32
        soil_moisture = bus.read_byte(ESP32_I2C_ADDRESS)
        return soil_moisture
    except Exception as e:
        print(f"Error reading from ESP32: {e}")
        return None

while True:
    # Read and print the soil moisture percentage
    moisture = read_soil_moisture()
    if moisture is not None:
        print(f"Soil Moisture: {moisture}%")
    else:
        print("Failed to read soil moisture")
    
    time.sleep(10)  # Increase delay between reads to allow ESP32 to update
