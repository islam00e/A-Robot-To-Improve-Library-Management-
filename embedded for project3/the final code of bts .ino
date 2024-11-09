#include <ros.h>
#include <geometry_msgs/Point32.h>
#include <geometry_msgs/Twist.h>
#include <Encoder.h>

// Define BTS7960B pins
const int motorLPWM = 3; // PWM pin for left motor speed control
const int motorLDir1 = 4; // Direction pin 1 for left motor
const int motorLDir2 = 5; // Direction pin 2 for left motor
const int motorRPWM = 6; // PWM pin for right motor speed control
const int motorRDir1 = 7; // Direction pin 1 for right motor
const int motorRDir2 = 8; // Direction pin 2 for right motor

// Initialize Encoder objects
Encoder R_enc(19, 18); // Right motor encoder on pins 19 and 18
Encoder L_enc(21, 20); // Left motor encoder on pins 21 and 20
long RoldPosition  = -999;
long LoldPosition  = -999;

// Define robot parameters
#define L 0.33 // Distance between the wheels (in meters)
#define R 0.05 // Radius of the wheels (in meters)

// Variables for motor velocities
float vel = 0.0;
float omega = 0.0;
float VR, VL;

// ROS setup
ros::NodeHandle nh;
geometry_msgs::Point32 Point_msg;
ros::Publisher enc_pub("/encoder", &Point_msg);
ros::Subscriber<geometry_msgs::Twist> sub("/cmd_vel", &motors_cb);

// Function to control left motor
void controlLeftMotor(float velocity) {
    if (velocity > 0) {
        digitalWrite(motorLDir1, HIGH);
        digitalWrite(motorLDir2, LOW);
    } else {
        digitalWrite(motorLDir1, LOW);
        digitalWrite(motorLDir2, HIGH);
    }
    analogWrite(motorLPWM, abs(velocity));
}

// Function to control right motor
void controlRightMotor(float velocity) {
    if (velocity > 0) {
        digitalWrite(motorRDir1, HIGH);
        digitalWrite(motorRDir2, LOW);
    } else {
        digitalWrite(motorRDir1, LOW);
        digitalWrite(motorRDir2, HIGH);
    }
    analogWrite(motorRPWM, abs(velocity));
}

// Callback for receiving velocity commands
void motors_cb(const geometry_msgs::Twist& msg) {
    vel = msg.linear.x;
    omega = msg.angular.z;
    VR = (2 * vel + omega * L) / (2 * R);
    VL = (2 * vel - omega * L) / (2 * R);
    controlLeftMotor(VL);
    controlRightMotor(VR);
}

// Setup function
void setup() {
    pinMode(motorLPWM, OUTPUT);
    pinMode(motorLDir1, OUTPUT);
    pinMode(motorLDir2, OUTPUT);
    pinMode(motorRPWM, OUTPUT);
    pinMode(motorRDir1, OUTPUT);
    pinMode(motorRDir2, OUTPUT);
    nh.advertise(enc_pub);
    nh.subscribe(sub);
}

// Loop function
void loop() {
    long RnewPosition = R_enc.read();
    if (RnewPosition != RoldPosition) {
        RoldPosition = RnewPosition;
    }

    long LnewPosition = L_enc.read();
    if (LnewPosition != LoldPosition) {
        LoldPosition = LnewPosition;
    }

    Point_msg.x = RnewPosition;
    Point_msg.y = LnewPosition;
    enc_pub.publish(&Point_msg);

    nh.spinOnce();
    delay(10);
}
