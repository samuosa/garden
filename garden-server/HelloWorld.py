from flask import Flask
import RPi.GPIO as GPIO
import time

# Initialize Flask app
app = Flask(__name__)

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
FIRST_GPIO_PIN = 17     # GPIO 17 is pin number 11 on the Raspberry Pi header
GPIO.setup(FIRST_GPIO_PIN, GPIO.OUT)

# Define the /ping endpoint
@app.route('/ping', methods=['GET'])
def ping():
    try:
        # Send an impulse (turn pin on and off quickly)
        GPIO.output(FIRST_GPIO_PIN, GPIO.HIGH)
        time.sleep(0.5)  # Keep the pin high for 0.5 seconds
        GPIO.output(FIRST_GPIO_PIN, GPIO.LOW)
        return "Impulse sent to GPIO pin!", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

# Run the Flask app on port 5000
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()  # Clean up GPIO on exit
