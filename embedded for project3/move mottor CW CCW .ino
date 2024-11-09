int R_EN   = 2;
int L_EN   = 3;
int R_PWM  = 4;
int L_PWM  = 5;
void setup() {
  // put your setup code here, to run once:
 pinMode(R_EN ,OUTPUT);
 pinMode(L_EN ,OUTPUT);
 pinMode(R_PWM ,OUTPUT);
 pinMode(L_PWM ,OUTPUT);
 digitalWrite(L_EN,HIGH);
 digitalWrite(R_EN,HIGH);
}

void loop() {
  // put your main code here, to run repeatedly:
 digitalWrite(R_PWM,0);
 digitalWrite(L_PWM,255);
}