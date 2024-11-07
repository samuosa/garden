#!/bin/bash

# Get current date in the format tt-mm-yy
DATE=$(date +"%d-%m-%y")

# Define the log file path
LOG_FILE="/home/admin/logs/logs-$DATE.log"

# Change to the project directory
cd ./garden

# Activate the virtual environment
source ./bin/activate

# Install dependencies
pip install -r ./src/requirements.txt

# Start the Python application and redirect both stdout and stderr to the log file
python src/App.py >> "$LOG_FILE" 2>&1

#mkdir logs
#sudo nano /etc/systemd/system/flask.service
#nano startup_flask.sh
#sudo nano /etc/systemd/system/flask.service
#chmod 755 startup_flask.sh 

#sudo systemctl enable flask.service
#sudo systemctl start flask.service
#sudo systemctl status flask.service