# App.py
from flask import Flask, jsonify
from flask_cors import CORS
from read_bme import readBme
from datetime import datetime

app = Flask(__name__)

CORS(app)

# Endpoint to get air
@app.route('/air', methods=['GET'])
def get_air_endpoint():
    (temp,hum,pr) = readBme()
    print(f"Temperature: {temp} Humidity: {hum} Pressure: {pr}")
    if temp is not None:
        return jsonify({
            'temperature': temp,
            'humidity': hum,
            'pressure': pr
          }), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to read temperature'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
