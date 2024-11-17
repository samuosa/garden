import RPi.GPIO as GPIO
import time
import csv
from datetime import datetime
import os
import sys

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setwarnings(False)

# Define GPIO pins for Motor 1
ENA = 13  # Enable pin for Motor 1 (PWM)
IN1 = 19  # Forward pin for Motor 1
IN2 = 26  # Backward pin for Motor 1

# Set up GPIO pins
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Set up PWM on ENA
pwm_ena = GPIO.PWM(ENA, 100)  # 100 Hz frequency
pwm_ena.start(0)  # Start with 0% duty cycle

# Define the pumping rate
PUMP_RATE = 1.926  # ml per second

def pump(ml, power=50):
    """Activate the pump to dispense a specified amount in ml at a specified power level."""
    # Calculate the required duration in seconds
    seconds = ml / PUMP_RATE


    print(f"Starting pump to dispense {ml} ml ({seconds:.2f} seconds) at {power}% power")

    # Set motor direction to forward
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm_ena.ChangeDutyCycle(power)  # Set power level

    # Keep the pump on for the calculated duration
    time.sleep(seconds)

    # Stop the pump
    pwm_ena.ChangeDutyCycle(0)
    print("Pump stopped")

    # Log the event to the CSV file
    log_pump_action(ml, power)

def log_pump_action(ml, power):
    """Log the pump activation time, dispensed volume in ml, and power level to watering.csv."""
    # Check if the CSV file exists
    file_exists = os.path.isfile('watering.csv')
    
    with open('watering.csv', mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        
        # Write the header if the file does not exist
        if not file_exists:
            writer.writerow(['timestamp', 'volume_ml', 'power'])
        
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Write the timestamp, volume, and power level to the CSV
        writer.writerow([timestamp, ml, power])
        print(f"Logged pump action: {timestamp} - {ml} ml at {power}% power")

# Read command-line arguments
#if len(sys.argv) < 3:
#    print("Usage: python script.py <volume_ml> <power>")
#    sys.exit(1)
#
#try:
#    # Parse command-line arguments
#    ml = float(sys.argv[1])      # First argument: volume in ml
#    power = int(sys.argv[2])     # Second argument: power level
#
#    # Call the pump function with the parsed arguments
#    pump(ml, power)
#finally:
#    # Clean up GPIO and stop PWM
#    pwm_ena.stop()
#    GPIO.cleanup()

 # Clean up GPIO and stop PWM
def cleanupPump():   
    pwm_ena.stop()
    GPIO.cleanup()
