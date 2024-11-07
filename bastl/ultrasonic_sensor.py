# ultrasonic_sensor.py

import time
from gpio_control import GPIO

# Import the GPIO setup from your gpio_control module if applicable
# from gpio_control import GPIO

# Set GPIO mode (if not set elsewhere)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define GPIO pins for the HC-SR04
ULTRASONIC_TRIGGER_PIN = 20  # Adjust to your setup
ULTRASONIC_ECHO_PIN = 21     # Adjust to your setup

# Set up GPIO pins
GPIO.setup(ULTRASONIC_TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ULTRASONIC_ECHO_PIN, GPIO.IN)

def measure_distance():
    # Ensure that the trigger pin is set to LOW
    GPIO.output(ULTRASONIC_TRIGGER_PIN, False)
    time.sleep(0.1)  # Allow sensor to settle

    # Send a 10µs pulse to trigger
    GPIO.output(ULTRASONIC_TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(ULTRASONIC_TRIGGER_PIN, False)

    StartTime = time.time()
    StopTime = time.time()

    # Save StartTime
    timeout = StartTime + 0.05  # 50ms timeout
    while GPIO.input(ULTRASONIC_ECHO_PIN) == 0 and StartTime < timeout:
        StartTime = time.time()
    if StartTime >= timeout:
        print("Timeout waiting for echo to go high")
        return None

    # Save time of arrival
    timeout = time.time() + 0.05  # 50ms timeout
    while GPIO.input(ULTRASONIC_ECHO_PIN) == 1 and StopTime < timeout:
        StopTime = time.time()
    if StopTime >= timeout:
        print("Timeout waiting for echo to go low")
        return None

    # Calculate time difference
    TimeElapsed = StopTime - StartTime
    # Calculate distance in centimeters
    distance = (TimeElapsed * 34300) / 2  # Speed of sound = 34300 cm/s

    return distance

def calculate_fill_level(measured_distance, max_distance, min_distance):
    if measured_distance is None:
        return None
    # Clamp measured distance within the min and max distances
    measured_distance = max(min(measured_distance, max_distance), min_distance)
    # Calculate fill level percentage
    fill_level = ((max_distance - measured_distance) / (max_distance - min_distance)) * 100
    return fill_level

def get_tank_fill_level():
    try:
        measured_distance = measure_distance()
        if measured_distance is None:
            return None
        # Adjust these values based on your tank's dimensions
        max_distance = 18.0  # Distance from sensor to bottom when empty (cm)
        min_distance = 1.0   # Distance from sensor to water surface when full (cm)

        fill_level = calculate_fill_level(measured_distance, max_distance, min_distance)
        return fill_level
    except Exception as e:
        print("Error in measuring tank fill level:", e)
        return None
#if __name__ == '__main__':
#    print("Tank fill level: {}%".format(get_tank_fill_level()))