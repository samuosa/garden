import smbus
import time

# I2C address of the ESP32 (make sure it matches the address in the ESP32 code)
I2C_ADDRESS = 0x04
bus = smbus.SMBus(1)  # Use I2C bus 1 on the Raspberry Pi

def read_soil_moisture():
    try:
        # Request one byte of data from the ESP32
        soil_moisture_percent = bus.read_byte(I2C_ADDRESS)
        
        # Print the soil moisture percentage
        print(f"Soil Moisture: {soil_moisture_percent}%")
    except OSError as e:
        print("Failed to read from the ESP32:", e)

while True:
    read_soil_moisture()
    time.sleep(1)  # Delay between readings
