#include <Arduino.h>

const int enablePin = 9;    // PWM pin for motor speed control
const int int1Pin = 8;      // Motor driver input 1
const int int2Pin = 7;      // Motor driver input 2

int speed = 150;            // Default speed setting

int encoderPin1 = 2;
int encoderPin2 = 3;

volatile long encoderValue = 0;

int pulsesPerRevolution = 0;

long maximumEncoderValue = 0;
int gearRatio = 1;          // Default to 1 to prevent division by zero
int antennaAngle = 0;
int newPulses = 0;

void setup() {
  Serial.begin(9600);
  pinMode(enablePin, OUTPUT);
  pinMode(int1Pin, OUTPUT);
  pinMode(int2Pin, OUTPUT);

  pinMode(encoderPin1, INPUT_PULLUP);
  pinMode(encoderPin2, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(encoderPin1), updateEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPin2), updateEncoder, CHANGE);
}

void loop() {
 {
  Serial.println(encoderValue);
  delay(1000); //just here to slow down the output, and show it will work  even during a delay

  Serial.println(maximumEncoderValue);
  delay(1000);
}
  
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    switch (command) {
      case 'A':  // Set Antenna Angle
        antennaAngle = Serial.parseInt();
        Serial.print("Received Antenna Angle: ");
        Serial.println(antennaAngle);
        break;
      case 'P':  // Set Pulse Count per Revolution
        newPulses = Serial.parseInt();
        Serial.print("Pulse count per revolution: ");
        Serial.println(newPulses);
        break;
      case 'G':  // Set Gear Ratio
        gearRatio = Serial.parseInt();
        Serial.print("Gear Ratio: ");
        Serial.println(gearRatio);
        break;
      case 'F':  // Forward
        forward(speed);
        Serial.println("Forward direction");
        break;
      case 'B':  // Backward
        backward(speed);
        Serial.println("Backward direction");
        break;
      case 'D':  // Direction Check
        directionCheck(encoderValue);
        break;
      case 'R':  // Reset
        reset();
        break;
      default:
        Serial.print("Unknown command: ");
        Serial.println(command);
        break;
    }
  }
}

void conversion(){
  long pulsesPerRevolution = newPulses * 4;
  maximumEncoderValue = pulsesPerRevolution * gearRatio / 360;
}

void updateEncoder() {
  static int lastEncoded = 0;
  int MSB = digitalRead(encoderPin1);
  int LSB = digitalRead(encoderPin2);
  int encoded = (MSB << 1) | LSB;
  int sum = (lastEncoded << 2) | encoded;

  if (sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011)
    encoderValue++;
  if (sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000)
    encoderValue--;

  lastEncoded = encoded;
}


void forward(int speed) {
  long targetEncoderValue = encoderValue + maximumEncoderValue;
  stopRequested = false;  // reset before starting

  while (encoderValue <= targetEncoderValue && !stopRequested) {
    analogWrite(enablePin, speed);
    digitalWrite(int1Pin, HIGH);
    digitalWrite(int2Pin, LOW);
    Serial.println("motor running in CW Direction \n");

    // Check if stop is pressed
    if (stopRequested) {
      break;  // quit the loop if pressed
    }
  }

  stopMotor();  // stop after the motor completes the loop
}

void backward(int speed) {
  long targetEncoderValue = encoderValue - maximumEncoderValue;
  stopRequested = false;    //reset before starting
  
  while (encoderValue >= targetEncoderValue && !stopRequested) {
    analogWrite(enablePin, speed);
    digitalWrite(int1Pin, LOW);
    digitalWrite(int2Pin, HIGH);
    Serial.println("motor running in CCW Direction \n");

    //Check if stop is pressed
    if (stopRequested) {
      break;    //quit the loop if pressed
    }
  }
  
  stopMotor();    //stop after the motor completes the loop
}

void stopMotor() {
  digitalWrite(int1Pin, LOW);
  digitalWrite(int2Pin, LOW);
  Serial.println("motor stopped");
}

void directionCheck(long currentEncoderValue) {
  static long previousEncoderValue = 0;

  if (currentEncoderValue > previousEncoderValue) {
    Serial.println("Clockwise Direction");
  } else if (currentEncoderValue < previousEncoderValue) {
    Serial.println("Anti-Clockwise Direction");
  } else {
    Serial.println("No Change in Direction");
  }
  previousEncoderValue = currentEncoderValue;
}

void reset() {
  while (encoderValue >= 0) {
    analogWrite(enablePin,255);
    digitalWrite(int1Pin, LOW);
    digitalWrite(int2Pin, HIGH);
    Serial.println("!!RESETTING THE ANTENNA POSITIONS!!!");
  }
  stopMotor();

  Serial.println("Parameters reset. Antenna returned to original position.");
}
