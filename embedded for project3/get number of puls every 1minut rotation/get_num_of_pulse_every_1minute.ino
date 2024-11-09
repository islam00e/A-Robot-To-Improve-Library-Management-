#include <Encoder.h>

#define ENCODER_A 2
#define ENCODER_B 3

#define RPWM 5      // Right PWM pin
#define LPWM 6      // Left PWM pin
#define R_EN 7      // Right enable pin
#define L_EN 8      // Left enable pin

Encoder motorEncoder(ENCODER_A, ENCODER_B);

void setup() {
  // Motor driver pin setup
  pinMode(RPWM, OUTPUT);
  pinMode(LPWM, OUTPUT);
  pinMode(R_EN, OUTPUT);
  pinMode(L_EN, OUTPUT);

  // Enable motor driver
  digitalWrite(R_EN, HIGH);
  digitalWrite(L_EN, HIGH);

  Serial.begin(9600); // Initialize serial communication

  // Initialize encoder position to 0
  motorEncoder.write(0);

  Serial.println("Setup complete. Motor will start rotating...");
}

void loop() {
  // Start the motor
  int motorSpeed = 200; // Speed value between 0 and 255
  setMotorSpeed(motorSpeed, true); // True for forward, false for reverse

  long startTime = millis();
  long pulseCount = 0;

  // Run the motor for 1 minute
  while (millis() - startTime < 60000) {
    pulseCount = motorEncoder.read();
    // Print the current pulse count every second for debugging
    if ((millis() - startTime) % 1000 == 0) {
      Serial.print("Current pulses: ");
      Serial.println(pulseCount);
    }
  }

  // Stop the motor
  setMotorSpeed(0, true);

  // Final pulse count after 1 minute
  pulseCount = motorEncoder.read();
  Serial.print("Pulses in the last minute: ");
  Serial.println(pulseCount);

  // Reset the encoder count
  motorEncoder.write(0);

  delay(5000); // Delay before next measurement (adjust as needed)
}

void setMotorSpeed(int speed, bool forward) {
  if (forward) {
    analogWrite(RPWM, speed);
    analogWrite(LPWM, 0);
  } else {
    analogWrite(RPWM, 0);
    analogWrite(LPWM, speed);
  }
}
