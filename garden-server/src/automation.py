# automation.py
import time
from gpio_control import control_pump
from read_esp import read_soil_moisture

soil_moisture_threshold = 30  # Moisture percentage threshold

def automation_loop(automation_event):
    while not automation_event.is_set():
        moisture = read_soil_moisture()
        if moisture is not None and moisture < soil_moisture_threshold:
            # Turn on the pump
            control_pump(1, 'on')
        else:
            # Turn off the pump
            control_pump(1, 'off')
        # Wait for 60 seconds or until automation_event is set
        automation_event.wait(timeout=60)
