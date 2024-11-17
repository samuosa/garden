#include <Wire.h> 
#include <driver/adc.h>

const int AirValue = 3570;  // Calibrated dry value (dry air)
const int WaterValue = 1186; // Calibrated wet value (fully wet)
const int SensorPin = 34;   // Analog pin connected to the soil moisture sensor

int soilMoistureValue = 0;
int soilmoisturepercent = 0;

#define I2C_ADDRESS 0x04  // I2C address for the ESP32 as a slave

void setup() {
  Serial.begin(115200);
  Wire.begin(I2C_ADDRESS);         
  Wire.onRequest(requestEvent);    
  pinMode(SensorPin, INPUT);       
  
  // Configure ADC
  analogSetPinAttenuation(SensorPin, ADC_11db);  // For input voltages up to ~3.3V
  analogReadResolution(12);                      // Set ADC resolution to 12 bits
}

void loop() {
  soilMoistureValue = readSoilMoisture();
  
  // Calculate the soil moisture percentage
  soilmoisturepercent = map(soilMoistureValue, AirValue, WaterValue, 0, 100);
  soilmoisturepercent = constrain(soilmoisturepercent, 0, 100);

  // Print the values for debugging
  Serial.print("Soil Moisture Raw ADC: ");
  Serial.print(soilMoistureValue);
  Serial.print(" | Soil Moisture Percent: ");
  Serial.println(soilmoisturepercent);

  delay(1000);  // Delay between readings
}

int readSoilMoisture() {
  int totalValue = 0;
  const int numReadings = 10;
  for (int i = 0; i < numReadings; i++) {
    totalValue += analogRead(SensorPin);
    delay(10);
  }
  return totalValue / numReadings;
}

void requestEvent() {
  Wire.write(soilmoisturepercent);  // Send the moisture percentage (0-100)
}
