import csv
import time
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import threading
from threading import Event
from datetime import datetime
import atexit
import schedule

from read_bme import readBme
from pump import pump,cleanupPump
from camera_handler import CameraHandler

app = Flask(__name__)
CORS(app)
camera_handler = CameraHandler()

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

def automate_pump():
    """
    Background thread to run scheduled tasks for automating the pump.
    """
    while not automation_event.is_set():
        schedule.run_pending()
        time.sleep(60)  # Check every minute for scheduled tasks

def save_picture():
    """
    Save a picture to ./pictures/${dateDD-MM-YY}growth.png every day at 16:00.
    """
    timestamp = datetime.now().strftime("%d-%m-%y")
    img_bytes = camera_handler.capture_picture()
    if img_bytes:
        with open(f'./pictures/{timestamp}growth.png', 'wb') as img_file:
            img_file.write(img_bytes)
        print(f"Saved picture: ./pictures/{timestamp}growth.png")
    else:
        print("Failed to capture image.")

# Schedule pump automation tasks
schedule.every().day.at("04:00").do(lambda: pump(50))
schedule.every().day.at("18:00").do(lambda: pump(50))

# Schedule picture automation task
schedule.every().day.at("16:00").do(save_picture)


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
# POST Endpoint to pump a specified amount in ml
@app.route('/pump', methods=['POST'])
def pump_endpoint():
    data = request.get_json()
    if not data or 'ml' not in data:
        return jsonify({'status': 'error', 'message': 'Amount in ml is required'}), 400

    ml = data['ml']
    pump(ml)
    return jsonify({'status': 'success', 'message': f'Pumped {ml} ml'}), 200

# GET Endpoint to retrieve all watering actions
@app.route('/watering', methods=['GET'])
def get_watering():
    watering_log = []
    try:
        with open('./watering.csv', mode='r') as file:
            reader = csv.reader(file, delimiter=';')
            next(reader, None)  # Skip the header row
            for row in reader:
                if len(row) == 3:
                    print(row)
                    timestamp, volume_ml, power = row
                    print(timestamp)
                    watering_log.append({
                        'timestamp': timestamp,
                        'volume': volume_ml
                    })
                    print(watering_log)
    except FileNotFoundError:
        return jsonify({'status': 'error', 'message': 'No watering records found'}), 404

    print(watering_log)
    return jsonify(watering_log), 200


@app.route('/picture', methods=['GET'])
def get_picture():
    img_bytes = camera_handler.capture_picture()
    if img_bytes:
        return Response(img_bytes, mimetype='image/jpeg')
    else:
        return Response("Failed to capture image.", status=500)
    

if __name__ == '__main__':
    # Start the background thread to save readings every 10 minutes
    background_thread = threading.Thread(target=save_readings_to_csv, daemon=True)
    background_thread.start()
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)

@atexit.register
def cleanupFlask():
    automation_event.set()
    cleanupPump()
    camera_handler.close_camera()
