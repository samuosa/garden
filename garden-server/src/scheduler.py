import schedule
import time
import threading
from datetime import datetime
from db import create_db_connection, save_reading_to_db
from read_esp import read_soil_moisture
from read_bme import readBme


def scheduled_sensor_reading():
    connection = create_db_connection()
    if connection is None:
        print("Database connection failed")
        return

    try:
        # Read sensor data
        temp, hum, pr = readBme()
        soil_moisture = read_soil_moisture()

        # Get the current timestamp
        timestamp = datetime.now()

        # Save to database
        save_reading_to_db(connection, timestamp, temp, hum, pr, soil_moisture)
    finally:
        if connection.is_connected():
            connection.close()

# Schedule the function to run every 5 minutes
schedule.every(5).minutes.do(scheduled_sensor_reading)

# Start the scheduler in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()
