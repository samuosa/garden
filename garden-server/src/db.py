import mysql.connector
from mysql.connector import Error

def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='sensor_data',
            user='flask',
            password='test'  # Replace with your actual password
        )
        if connection.is_connected():
            print("Connected to MariaDB database")
            return connection
    except Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return None

def save_reading_to_db(connection, timestamp, temperature=None, humidity=None, pressure=None, soil_moisture=None):
    try:
        cursor = connection.cursor()
        sql_insert_query = """INSERT INTO readings (timestamp, temperature, humidity, pressure, soil_moisture)
                              VALUES (%s, %s, %s, %s, %s)"""
        record = (timestamp, temperature, humidity, pressure, soil_moisture)
        cursor.execute(sql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into readings table")
    except Error as e:
        print(f"Failed to insert into MySQL table {e}")
