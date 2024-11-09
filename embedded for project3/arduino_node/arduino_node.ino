// Pin definitions
const int R_PWM2 = 6;
const int L_PWM2 = 7;
const int EN2 = 20;

const int R_PWM1 = 4;
const int L_PWM1 = 5;
const int EN1 = 21;
// Motor speed (0 - 255)
int motorSpeed = 200;

void setup() {
  pinMode(R_PWM2, OUTPUT);
  pinMode(L_PWM2, OUTPUT);
  pinMode(EN2, OUTPUT);
  pinMode(R_PWM1, OUTPUT);
  pinMode(L_PWM1, OUTPUT);
  pinMode(EN1, OUTPUT);
 
}

void loop() {
  // Enable motor driver
   digitalWrite(EN2, HIGH);
digitalWrite(EN1, HIGH);
  // Motor forward
  delay(5000);

  analogWrite(R_PWM2, motorSpeed);
  analogWrite(L_PWM2, 0);
  analogWrite(R_PWM1, motorSpeed);
  analogWrite(L_PWM1, 0);
  delay(1000);
analogWrite(R_PWM2, 0);
  analogWrite(L_PWM2, motorSpeed);
  analogWrite(R_PWM1, 0);
  analogWrite(L_PWM1, 0);
  delay(1000);
  
}