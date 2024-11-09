// Pin definitions
const int R_PWM = 6;
const int L_PWM = 7;
const int EN = 20;

const int R_PWM1 = 4;
const int L_PWM1 = 5;
const int EN1 = 21;
// Motor speed (0 - 255)
int motorSpeed = 255;

void setup() {
  pinMode(R_PWM, OUTPUT);
  pinMode(L_PWM, OUTPUT);
  pinMode(EN, OUTPUT);
  pinMode(R_PWM1, OUTPUT);
  pinMode(L_PWM1, OUTPUT);
  pinMode(EN1, OUTPUT);
 
}

void loop() {
  // Enable motor driver
   digitalWrite(EN, HIGH);
digitalWrite(EN1, HIGH);
  // Motor forward
  analogWrite(R_PWM, 0);
  analogWrite(L_PWM, motorSpeed);
  analogWrite(R_PWM1, 0);
  analogWrite(L_PWM1, motorSpeed);
  delay(10000);

  /*// Motor stop
  analogWrite(R_PWM, 0);
  analogWrite(L_PWM, 0);
  delay(2000);

  // Motor reverse
  analogWrite(R_PWM, 0);
  analogWrite(L_PWM, motorSpeed);
  delay(10000);
*/
  // Disable motor driver (optional, if you want to turn off the driver
  // completely) digitalWrite(EN, LOW); delay(2000);
}