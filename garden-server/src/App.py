# App.py
from flask import Flask, request, jsonify, Response, send_file
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
import threading
import atexit
from threading import Event

from gpio_control import GPIO, control_pump, control_ventilator, cleanup
from read_esp import read_soil_moisture
from automation import automation_loop
from read_bme import readBme
from read_fill import get_tank_fill_level
from camera_handler import CameraHandler  # Assuming the class is in camera_handler.py
from datetime import datetime
from db import create_db_connection, save_reading_to_db

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = '1b7f0a6f811ea8c623744c17464d52401c018eb5397926d2522ad288431238b34654333fc913c29cdc05df1e42fb511f3eb4dbd12347ce43b5235014b8e2aec22ed32fc40abd7ff6b78bd980107b32fe1c334b715069919e5cfc0ebd441c47411f47d64fea01ba7cfe6c62738e5db667533cc6c8cd6ea4c38f8ece8fb14608fedf27d545ace51628281fd8a49781d0e6d02c70659e6ce4231909e91bdff054a92e653d53f8e32ff89606eed73fc323fe22a5426c34bfeae1e64e892e414c028a07b1d663b3c14f64fb70aca3e20100e5d444e72544c29a0f3894bb574056e66dd39e2f539ae5d22780ff6b6c45c34b565194428337ce8455341189ed4530fce8'  # Replace with a secure secret key!
jwt = JWTManager(app)
CORS(app)
camera_handler = CameraHandler()

# Event to control the automation loop
automation_event = Event()

users = {
    'samu': 'root'
}

# Endpoint for user login and token generation
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'msg': 'Missing username or password'}), 400
    print(data)
    username = data['username']
    password = data['password']

    if username in users and users[username] == password:
        # Create a new token with the user identity
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'msg': 'Bad username or password'}), 401


@app.route('/read_sensors', methods=['GET'])
@jwt_required()
def read_sensors():
    connection = create_db_connection()
    if connection is None:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

    try:
        # Read sensor data
        temp, hum, pr = readBme()
        soil_moisture = read_soil_moisture()

        fil_level = get_tank_fill_level()

        # Get the current timestamp
        timestamp = datetime.now()

        # Save to database
        save_reading_to_db(connection, timestamp, temp, hum, pr, soil_moisture)

        # Return the readings
        return jsonify({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': temp,
            'humidity': hum,
            'pressure': pr,
            'soil_moisture': soil_moisture,
            'fill_level': fil_level
        }), 200
    finally:
        if connection.is_connected():
            connection.close()

# Endpoint to control pumps
@app.route('/pump', methods=['POST'])
@jwt_required()
def pump_endpoint():
    data = request.get_json()
    pump_id = data.get('pump_id')
    action = data.get('action')

    try:
        control_pump(pump_id, action)
        return jsonify({'status': 'success'}), 200
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Endpoint to get air
@app.route('/air', methods=['GET'])
@jwt_required()
def get_air_endpoint():
    (temp,hum,pr) = readBme()
    if temp is not None:
        return jsonify({
            'temperature': temp,
            'humidity': hum,
            'pressure': pr
          }), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to read temperature'}), 500

# Endpoint to get soil moisture
@app.route('/soil_moisture', methods=['GET'])
@jwt_required()
def get_soil_moisture_endpoint():
    moisture = read_soil_moisture()
    if moisture is not None:
        return jsonify({'soil_moisture': moisture}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to read soil moisture'}), 500

# Endpoint to control ventilators
@app.route('/ventilator', methods=['POST'])
@jwt_required()
def ventilator_endpoint():
    data = request.get_json()
    vent_id = data.get('vent_id')
    action = data.get('action')

    try:
        control_ventilator(vent_id, action)
        return jsonify({'status': 'success'}), 200
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Endpoint to enable or disable automation
@app.route('/automation', methods=['POST'])
@jwt_required()
def set_automation():
    data = request.get_json()
    action = data.get('action')
    if action == 'enable':
        automation_event.clear()
        # Start the automation thread if not already running
        if not automation_thread.is_alive():
            automation_thread.start()
        return jsonify({'status': 'success', 'message': 'Automation enabled'}), 200
    elif action == 'disable':
        automation_event.set()
        return jsonify({'status': 'success', 'message': 'Automation disabled'}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid action'}), 400

@app.route('/fill_level', methods=['GET'])
@jwt_required()
def get_fill_level_endpoint():
    fill_level = get_tank_fill_level()
    if fill_level is not None:
        return jsonify({'fill_level': fill_level}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to read tank fill level'}), 500



@app.route('/picture', methods=['GET'])
def get_picture():
    img_bytes = camera_handler.capture_picture()
    if img_bytes:
        return Response(img_bytes, mimetype='image/jpeg')
    else:
        return Response("Failed to capture image.", status=500)
    

## Clean after request thread
#@app.teardown_appcontext
#def teardown(exception=None):
#    #request 


@atexit.register
def cleanupFlask():
    automation_event.set()
    cleanup()
    camera_handler.close_camera()

if __name__ == '__main__':
    automation_thread = threading.Thread(target=automation_loop, args=(automation_event,))
    automation_thread.daemon = True  # Daemonize thread
    automation_thread.start()
    app.run(host='0.0.0.0', port=5000)
