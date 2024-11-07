#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const int AirValue = 790;   // Value for dry air
const int WaterValue = 390; // Value for water (fully saturated soil)
const int SensorPin = 35;   // Analog pin connected to the soil moisture sensor

int soilMoistureValue = 0;
int soilmoisturepercent = 0;

#define I2C_ADDRESS 0x04  // I2C address for the ESP32 as a slave

void setup() {
  Serial.begin(115200);
  Wire.begin(I2C_ADDRESS);         // Initialize I2C as a slave
  Wire.onRequest(requestEvent);    // Register the request event
  pinMode(SensorPin, INPUT);       // Set up the soil moisture sensor pin
}

void loop() {
  // Read the analog soil moisture sensor value
  soilMoistureValue = analogRead(SensorPin);
  Serial.println(soilMoistureValue);

  // Map the sensor value to a percentage (0 to 100%)
  soilmoisturepercent = map(soilMoistureValue, AirValue, WaterValue, 0, 100);

  // Ensure soil moisture percent is within 0-100%
  if (soilmoisturepercent > 100) {
    soilmoisturepercent = 100;
  } else if (soilmoisturepercent < 0) {
    soilmoisturepercent = 0;
  }

  delay(1000);  // Delay for readability in serial output
}

// I2C request event: provides the soil moisture percentage to the I2C master
void requestEvent() {
  Wire.write(soilmoisturepercent);  // Send the moisture percentage (0-100)
}
