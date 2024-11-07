import smbus

I2C_ADDRESS = 0x04  # The same address used in your ESP32 code
bus = smbus.SMBus(1)  # Use I2C bus 1 on Raspberry Pi

def read_soil_moisture():
    try:
        # Read one byte of data
        moisture = bus.read_byte(I2C_ADDRESS)
        return moisture
    except Exception as e:
        print(f"Error reading from I2C device: {e}")
        return None
