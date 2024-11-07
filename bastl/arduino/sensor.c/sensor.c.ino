#include <Wire.h>

const int AirValue = 790;   // Value for dry air
const int WaterValue = 390; // Value for water (fully saturated soil)
const int SensorPin = A0;   // Analog pin connected to the soil moisture sensor

int soilMoistureValue = 0;
int soilMoisturePercent = 0;

void setup() {
  Serial.begin(9600);
  Wire.begin(0x04);         // Initialize I2C with address 0x04 for Arduino as a slave
  Wire.onRequest(requestEvent); // Register the request event
  pinMode(SensorPin, INPUT);    // Set up the soil moisture sensor pin
}

void loop() {
  // Read and calculate soil moisture
  soilMoistureValue = analogRead(SensorPin);
  soilMoisturePercent = map(soilMoistureValue, AirValue, WaterValue, 0, 100);

  // Constrain the percentage within the 0-100 range
  soilMoisturePercent = constrain(soilMoisturePercent, 0, 100);

  // Print soil moisture values to the Serial Monitor for debugging
  Serial.print("Soil Moisture Raw: ");
  Serial.print(soilMoistureValue);
  Serial.print(" | Soil Moisture Percent: ");
  Serial.println(soilMoisturePercent);

  delay(1000); // Wait a second between readings
}

// I2C request event: sends the soil moisture percentage to the I2C master
void requestEvent() {
  Wire.write(soilMoisturePercent); // Send the soil moisture percentage (0-100)
}
