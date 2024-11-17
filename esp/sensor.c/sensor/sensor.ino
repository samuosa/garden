#include <Wire.h> 
#include <driver/adc.h>

const int AirValue = 3570;  // Calibrated dry value (dry air)
const int WaterValue = 970; // Calibrated wet value (fully wet)
const int SensorPin = 34;   // Analog pin connected to the soil moisture sensor

int soilMoistureValue = 0;
int soilmoisturepercent = 0;

#define I2C_ADDRESS 0x04  // I2C address for the ESP32 as a slave
#define SDA_PIN 16     // GPIO 16 as SDA
#define SCL_PIN 17     // GPIO 17 as SCL

// Pump control parameters
#define NUM_PUMPS 6

// Define the GPIO pins for the pumps
// For each pump, we need an enable pin (PWM) and direction pins
struct Pump {
  int enablePin;
  int in1Pin;
  int in2Pin;
};

// Define the pins for each pump
Pump pumps[NUM_PUMPS] = {
  {13, 12, 14},  // Pump 1: ENA, IN1, IN2
  {27, 26, 25},  // Pump 2: ENB, IN3, IN4
  {33, 32, 15},  // Pump 3: ENA, IN1, IN2
  {21, 19, 18},  // Pump 4: ENB, IN3, IN4
  {5, 17, 16},   // Pump 5: ENA, IN1, IN2
  {4, 2, 0}      // Pump 6: ENB, IN3, IN4
};

void setup() {
  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN, I2C_ADDRESS);
  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
  pinMode(SensorPin, INPUT);

  // Configure ADC
  analogSetPinAttenuation(SensorPin, ADC_11db);  // For input voltages up to ~3.3V
  analogReadResolution(12);                      // Set ADC resolution to 12 bits

  // Initialize pump control pins
  for (int i = 0; i < NUM_PUMPS; i++) {
    // Set up enable pins for PWM
    ledcSetup(i, 5000, 8); // Channel i, frequency 5kHz, resolution 8 bits
    ledcAttachPin(pumps[i].enablePin, i); // Attach enable pin to PWM channel

    // Set direction pins
    pinMode(pumps[i].in1Pin, OUTPUT);
    pinMode(pumps[i].in2Pin, OUTPUT);

    // Set initial direction (e.g., forward)
    digitalWrite(pumps[i].in1Pin, HIGH);
    digitalWrite(pumps[i].in2Pin, LOW);
  }
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
  Serial.print("Soil Moisture returned: ");
  Serial.println(soilmoisturepercent);
}

void receiveEvent(int numBytes) {
  while (Wire.available() > 0) {
    int command = Wire.read();
    if (command == 0x02) { // Control pump command
      if (Wire.available() >= 4) {
        uint8_t pump_id = Wire.read();
        uint16_t duration = (Wire.read() << 8) | Wire.read(); // Duration in ms
        uint8_t power = Wire.read();

        controlPump(pump_id, duration, power);
      }
    }
    // Add more command handlers if needed
  }
}

void controlPump(uint8_t pump_id, uint16_t duration, uint8_t power) {
  // Validate pump_id
  if (pump_id < 1 || pump_id > NUM_PUMPS) {
    Serial.println("Invalid pump ID");
    return;
  }

  // Adjust pump_id to zero-based index
  uint8_t pumpIndex = pump_id - 1;

  // Calculate duty cycle based on power percentage (0-100%)
  uint8_t dutyCycle = map(constrain(power, 0, 100), 0, 100, 0, 255);

  // Set the PWM duty cycle on the enable pin to control speed/power
  ledcWrite(pumpIndex, dutyCycle);

  Serial.print("Pump ");
  Serial.print(pump_id);
  Serial.print(" started at power ");
  Serial.print(power);
  Serial.print("% for duration ");
  Serial.print(duration);
  Serial.println(" ms");

  // Delay for the specified duration (non-blocking)
  unsigned long startTime = millis();
  while (millis() - startTime < duration) {
    // You can perform other tasks here if needed
    delay(10); // Small delay to prevent watchdog reset
  }

  // Stop the pump after duration
  ledcWrite(pumpIndex, 0); // Set duty cycle to 0 to stop the pump

  Serial.print("Pump ");
  Serial.print(pump_id);
  Serial.println(" stopped");
}
