#include <PID_v1.h>
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

// Ultrasonic Sensor Pins
const int trigPins[] = {2, 3, 4, 5, 6, 7};
const int echoPins[] = {8, 9, 10, 11, 12, 13};
const int numSensors = 6;
long distances[numSensors];

// Motor Driver Pins
const int motor1Pin1 = 22; 
const int motor1Pin2 = 23; 
const int motor2Pin1 = 24; 
const int motor2Pin2 = 25; 
const int enableMotor1 = 26; 
const int enableMotor2 = 27; 

// Encoder Pins and Variables
const int encoderPin1 = 18; 
const int encoderPin2 = 19; 
volatile long encoderCount1 = 0;
volatile long encoderCount2 = 0;

// PID Variables
double setpoint1, input1, output1;
double setpoint2, input2, output2;
double Kp = 2.0, Ki = 5.0, Kd = 1.0;

// PID Controllers
PID motorPID1(&input1, &output1, &setpoint1, Kp, Ki, Kd, DIRECT);
PID motorPID2(&input2, &output2, &setpoint2, Kp, Ki, Kd, DIRECT);

// GPS Module
TinyGPSPlus gps;
HardwareSerial GPSSerial = Serial3;

// Bluetooth Module using Software Serial
SoftwareSerial bluetoothSerial(16, 17); // RX, TX pins

void setup() {
  // Initialize Ultrasonic Sensors
  for (int i = 0; i < numSensors; i++) {
    pinMode(trigPins[i], OUTPUT);
    pinMode(echoPins[i], INPUT);
  }

  // Initialize Motor Driver Pins
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enableMotor1, OUTPUT);
  pinMode(enableMotor2, OUTPUT);

  // Initialize Encoders
  attachInterrupt(digitalPinToInterrupt(encoderPin1), encoderISR1, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPin2), encoderISR2, CHANGE);

  // Initialize PID Controllers
  motorPID1.SetMode(AUTOMATIC);
  motorPID2.SetMode(AUTOMATIC);
  setpoint1 = 100; 
  setpoint2 = 100; 

  // Initialize GPS Module
  GPSSerial.begin(9600);

  // Initialize Bluetooth Module
  bluetoothSerial.begin(9600);
}

void loop() {
  // Read Ultrasonic Sensors
  for (int i = 0; i < numSensors; i++) {
    distances[i] = readUltrasonic(i);
  }

  // Update PID Controller Inputs
  input1 = encoderCount1;
  input2 = encoderCount2;

  // Compute PID Output
  motorPID1.Compute();
  motorPID2.Compute();

  // Set Motor Speeds
  analogWrite(enableMotor1, output1);
  analogWrite(enableMotor2, output2);

  // Read GPS Data
  while (GPSSerial.available() > 0) {
    if (gps.encode(GPSSerial.read())) {
      if (gps.location.isValid()) {
        double latitude = gps.location.lat();
        double longitude = gps.location.lng();

        // Send data via Bluetooth
        bluetoothSerial.print("Latitude: ");
        bluetoothSerial.print(latitude, 6);
        bluetoothSerial.print(", Longitude: ");
        bluetoothSerial.println(longitude, 6);
      }
    }
  }

  if (millis() > 5000 && gps.charsProcessed() < 10) {
    bluetoothSerial.println("No GPS detected");
  }

  // Implement any additional logic for robot control
}

long readUltrasonic(int sensorIndex) {
  digitalWrite(trigPins[sensorIndex], LOW);
  delayMicroseconds(2);
  digitalWrite(trigPins[sensorIndex], HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPins[sensorIndex], LOW);
  long duration = pulseIn(echoPins[sensorIndex], HIGH);
  return duration * 0.034 / 2;
}

void encoderISR1() {
  encoderCount1++;
}

void encoderISR2() {
  encoderCount2++;
}
