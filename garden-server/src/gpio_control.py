# gpio_control.py

import RPi.GPIO as GPIO

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
print("GPIO mode set to BCM:", GPIO.getmode())

# Define GPIO pins for pumps
PUMP1_IN1 = 23
PUMP1_IN2 = 24
PUMP2_IN3 = 27
PUMP2_IN4 = 22

# Define GPIO pins for ventilators
VENT1_PIN = 5
VENT2_PIN = 6

## Define GPIO pins for ultrasonic sensor
ULTRASONIC_TRIGGER_PIN = 20  # Adjust as per your wiring
ULTRASONIC_ECHO_PIN = 21     # Adjust as per your wiring

# Set up pump GPIO pins
GPIO.setup(PUMP1_IN1, GPIO.OUT)
GPIO.setup(PUMP1_IN2, GPIO.OUT)
GPIO.setup(PUMP2_IN3, GPIO.OUT)
GPIO.setup(PUMP2_IN4, GPIO.OUT)

# Set up ventilator GPIO pins
GPIO.setup(VENT1_PIN, GPIO.OUT)
GPIO.setup(VENT2_PIN, GPIO.OUT)

## Set up ultrasonic sensor GPIO pins
GPIO.setup(ULTRASONIC_TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ULTRASONIC_ECHO_PIN, GPIO.IN)
GPIO.output(ULTRASONIC_TRIGGER_PIN, False)

# Initialize pumps and ventilators to off
GPIO.output(PUMP1_IN1, GPIO.LOW)
GPIO.output(PUMP1_IN2, GPIO.LOW)
GPIO.output(PUMP2_IN3, GPIO.LOW)
GPIO.output(PUMP2_IN4, GPIO.LOW)
GPIO.output(VENT1_PIN, GPIO.LOW)
GPIO.output(VENT2_PIN, GPIO.LOW)

def control_pump(pump_id, action):
    try:
        if pump_id == 1:
            if action == 'on':
                GPIO.output(PUMP1_IN1, GPIO.HIGH)
                GPIO.output(PUMP1_IN2, GPIO.LOW)
            elif action == 'off':
                GPIO.output(PUMP1_IN1, GPIO.LOW)
                GPIO.output(PUMP1_IN2, GPIO.LOW)
            else:
                raise ValueError('Invalid action')
        elif pump_id == 2:
            if action == 'on':
                GPIO.output(PUMP2_IN3, GPIO.HIGH)
                GPIO.output(PUMP2_IN4, GPIO.LOW)
            elif action == 'off':
                GPIO.output(PUMP2_IN3, GPIO.LOW)
                GPIO.output(PUMP2_IN4, GPIO.LOW)
            else:
                raise ValueError('Invalid action')
        else:
            raise ValueError('Invalid pump ID')
    except Exception as e:
        raise e

def control_ventilator(vent_id, action):
    try:
        if vent_id == 1:
            GPIO.output(VENT1_PIN, GPIO.HIGH if action == 'on' else GPIO.LOW)
        elif vent_id == 2:
            GPIO.output(VENT2_PIN, GPIO.HIGH if action == 'on' else GPIO.LOW)
        else:
            raise ValueError('Invalid ventilator ID')
    except Exception as e:
        raise e

def cleanup():
    GPIO.cleanup()

# Export GPIO pins and control functions
__all__ = [
    'GPIO',
    'PUMP1_IN1',
    'PUMP1_IN2',
    'PUMP2_IN3',
    'PUMP2_IN4',
    'VENT1_PIN',
    'VENT2_PIN',
    'ULTRASONIC_TRIGGER_PIN',
    'ULTRASONIC_ECHO_PIN',
    'control_pump',
    'control_ventilator',
    'cleanup'
]
