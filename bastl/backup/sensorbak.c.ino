#include <Wire.h>

#define I2C_ADDRESS 0x04   // Custom I2C address for ESP32
#define SENSOR1_PIN 34     // Analog pin for Sensor 1
#define SENSOR2_PIN 35     // Analog pin for Sensor 2

// Calibration parameters (adjust these based on your sensor calibration)
const int AIR_VALUE = 790;   // Analog reading when sensor is dry (air)
const int WATER_VALUE = 390; // Analog reading when sensor is in water (fully wet)

// Map function to convert readings to percentage
int mapToPercentage(int value, int min, int max) {
  int percent = (value - min) * 100 / (max - min);
  return constrain(percent, 0, 100); // Constrain to 0-100%
}

void setup() {
  Wire.begin(I2C_ADDRESS);          // Initialize I2C as slave
  Wire.onRequest(requestEvent);     // Register event for data request from Pi
  pinMode(SENSOR1_PIN, INPUT);
  pinMode(SENSOR2_PIN, INPUT);
}

void loop() {
  // No code in the main loop as data will be sent upon request
}

void requestEvent() {
  // Read raw analog values from the sensors
  int sensor1_value = analogRead(SENSOR1_PIN);
  int sensor2_value = analogRead(SENSOR2_PIN);

  // Map to percentage based on calibration
  int sensor1_percent = mapToPercentage(sensor1_value, WATER_VALUE, AIR_VALUE);
  int sensor2_percent = mapToPercentage(sensor2_value, WATER_VALUE, AIR_VALUE);

  // Send percentage values as single bytes (0-100%)
  Wire.write(sensor1_percent);  // Send Sensor 1 moisture percentage
  Wire.write(sensor2_percent);  // Send Sensor 2 moisture percentage
}
