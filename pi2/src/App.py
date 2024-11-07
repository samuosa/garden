import csv
import time
from flask import Flask, jsonify
from flask_cors import CORS
import threading
from threading import Event
from datetime import datetime
from read_bme import readBme

app = Flask(__name__)
CORS(app)

# Event to control the background saving loop
automation_event = Event()

def save_readings_to_csv():
    """
    Background thread that saves sensor readings every 10 minutes to a CSV file.
    """
    while not automation_event.is_set():
        (temp, hum, pr) = readBme()
        if temp is not None and hum is not None and pr is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Append the readings to the CSV file
            with open('./readings.csv', mode='a', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow([timestamp, hum, temp, pr])
            print(f"Saved reading: {timestamp}, Humidity: {hum}, Temperature: {temp}, Pressure: {pr}")
        else:
            print("Failed to read sensor data.")
        # Wait for 10 minutes before the next reading
        automation_event.wait(600)

# Endpoint to get air
@app.route('/air', methods=['GET'])
def get_air_endpoint():
    (temp, hum, pr) = readBme()
    print(f"Temperature: {temp} Humidity: {hum} Pressure: {pr}")
    if temp is not None:
        return jsonify({
            'temperature': temp,
            'humidity': hum,
            'pressure': pr
        }), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to read temperature'}), 500


# Endpoint to get all readings
@app.route('/all_readings', methods=['GET'])
def get_all_readings():
    readings = []
    try:
        with open('./readings.csv', mode='r') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                if len(row) == 4:
                    timestamp, hum, temp, pr = row
                    readings.append({
                        'timestamp': timestamp,
                        'temperature': float(temp),
                        'humidity': float(hum),
                        'pressure': float(pr)
                    })
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': 'No readings found'}), 404
    
    return jsonify(readings), 200


if __name__ == '__main__':
    # Start the background thread to save readings every 10 minutes
    background_thread = threading.Thread(target=save_readings_to_csv, daemon=True)
    background_thread.start()
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
