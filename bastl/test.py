import smbus
import time

# I2C address of the ESP32 (make sure it matches the address in the ESP32 code)
I2C_ADDRESS = 0x04
bus = smbus.SMBus(1)  # Use I2C bus 1 on the Raspberry Pi

def read_soil_moisture():
    try:
        # Request one byte of data from the ESP32
        soil_moisture_percent = bus.read_byte(I2C_ADDRESS)
        
        # Print and return the soil moisture percentage
        print(f"Soil Moisture: {soil_moisture_percent}%")
        return soil_moisture_percent
    except OSError as e:
        print("Failed to read from the ESP32:", e)
        return None

def control_pump(pump_id, power, duration):
    try:
        # Prepare the command packet
        command = [0x02, pump_id, (duration >> 8) & 0xFF, duration & 0xFF, power]
        
        # Send the command packet to the ESP32
        bus.write_i2c_block_data(I2C_ADDRESS, 0, command)
        
        # Print confirmation
        print(f"Sent command to pump {pump_id}: Power={power}%, Duration={duration} ms")
        
    except OSError as e:
        print(f"Failed to send command to pump {pump_id}:", e)

# Main script loop
while True:
    # Read soil moisture level from the sensor
    sensor1 = read_soil_moisture()
    print(f"Sensor 1 Moisture Level: {sensor1}")

    # Activate Pump 1 at 50% power for 4 seconds (4000 ms)
    control_pump(pump_id=1, power=50, duration=4000)
    time.sleep(6)  # Wait for pump 1 to finish

    # Activate Pump 2 at 30% power for 2 seconds (2000 ms)
    control_pump(pump_id=2, power=30, duration=2000)
    time.sleep(4)  # Wait for pump 2 to finish

    # Wait a bit before the next soil moisture reading
    time.sleep(1)  # Delay between readings
