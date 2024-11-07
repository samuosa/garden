import bme280
import smbus2

port = 1
address = 0x76 # Adafruit BME280 address. Other BME280s may be different

def readBme():
    bus = smbus2.SMBus(port)

    bme280.load_calibration_params(bus,address)
    print("Reading BME280 sensor data...")
    try:
      bme280_data = bme280.sample(bus,address)

      # Compensate the raw data
      temperature = bme280_data.temperature
      pressure = bme280_data.pressure
      humidity = bme280_data.humidity

      # Print the results
      print(f"Temperature: {temperature:.2f} °C")
      print(f"Humidity: {humidity:.2f} %")
      print(f"Pressure: {pressure:.2f} hPa")
      return(temperature, humidity, pressure)
    finally:
        bus.close()

