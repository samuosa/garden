#!/bin/sh
python3 -m venv ./
source bin/activate
pip install flask
pip install smbus
pip install flask_cors
pip install RPi.GPIO
python App.py
