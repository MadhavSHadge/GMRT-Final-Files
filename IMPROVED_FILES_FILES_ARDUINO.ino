#include <Arduino.h>

const int enablePin = 9;    // PWM pin for motor speed control
const int int1Pin = 8;      // Motor driver input 1
const int int2Pin = 7;      // Motor driver input 2

int encoderPin1 = 2;    //Encoder pin 2, White
int encoderPin2 = 3;    //Encoder pin 3, Green

volatile long encoderValue = 0;
int pulsesPerRevolution = 0;        //encoder value that is PPM 
long maximumEncoderValue = 0;       //maximum value the encoder can go while rotating the antenna for 360 degree.
long requiredPulsesForRotation;       //pulses that are required to move antenna by requested angle

int gearRatio = 1;          // Default to 1 to prevent division by zero
int antennaAngle;       //store the antenna angle from python
int newPulses;        //store the ppm from python
int speed;        //store the value of speed that we get from arduino

bool stopRequested = false;     //for stopping the while loop 

void setup() {
  Serial.begin(9600);   //serial communication baudrate setting
  
  //motor pins declared as output
  pinMode(enablePin, OUTPUT);
  pinMode(int1Pin, OUTPUT);
  pinMode(int2Pin, OUTPUT);

  //turn on the internal pullup
  pinMode(encoderPin1, INPUT_PULLUP);
  pinMode(encoderPin2, INPUT_PULLUP);

  //keep the encoder to change for detection in the change of value
  attachInterrupt(digitalPinToInterrupt(encoderPin1), updateEncoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderPin2), updateEncoder, CHANGE);

  conversion();
}

void conversion(){        //converting the pulses to maximumEncoderValue we can get for 360 degree of rotation
  long pulsesPerRevolution = newPulses * 4;       //multiply it by 4 to get encoder count
  maximumEncoderValue = (pulsesPerRevolution * gearRatio);      //multiply it by gear ratio to get maximum pulses antenna can rotate
  requiredPulsesForRotation= (maximumEncoderValue / 360)*antennaAngle;        //pulses the antenna will rotate for
  Serial.println("Maximum Encoder Value is:- ");
  Serial.println(maximumEncoderValue);
  Serial.println("Required Pulses for Rotation is:- ");
  Serial.println(requiredPulsesForRotation);
}

void loop() {
 {
  Serial.println(encoderValue);
  delay(2000); //just here to slow down the output, and show it will work  even during a delay
}
  
  if (Serial.available() > 0) {
    char command = Serial.read();       //read commands that are being sent from python
    
    switch (command) {            //set the case as per the commands sent from the python gui
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
        
      case 'F':  // clockwise
        forward(speed, requiredPulsesForRotation);
        Serial.println("Forward direction");
        conversion();
        break;
        
      case 'B':  // anticlockwise
        backward(speed, requiredPulsesForRotation);
        Serial.println("Backward direction");
        conversion();
        break;
        
      case 'D':  // Direction Check
        directionCheck(encoderValue);
        break;
        
      case 'R':  // Reset the antenna position to zero
        reset (requiredPulsesForRotation);
        break;
        
      case 'S':   // Stop the motor
        analogWrite(enablePin, 0);
        Serial.println("Motor stopped.");
        break;
        
      case 'M':   //set speed i.e pwm in motor
        speed = Serial.parseInt();
        Serial.print("Speed Received : ");
        Serial.println(speed);
        break;
        
      default:      //handle unknown commands
        Serial.print("Unknown command: ");
        Serial.println(command);
        break;
    }
  }
}

void conversion(){        //converting the pulses to maximumEncoderValue we can get for 360 degree of rotation
  long pulsesPerRevolution = newPulses * 4;       //multiply it by 4 to get encoder count
  maximumEncoderValue = (pulsesPerRevolution * gearRatio);      //multiply it by gear ratio to get maximum pulses antenna can rotate
  requiredPulsesForRotation= (maximumEncoderValue / 360)*antennaAngle;        //pulses the antenna will rotate for
  Serial.println("Maximum Encoder Value is:- ");
  Serial.println(maximumEncoderValue);
  Serial.println("Required Pulses for Rotation is:- ");
  Serial.println(requiredPulsesForRotation);
}

void updateEncoder() {        //arduino counting using A and B pulse from the encoder  !!do not change!!
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

void forward(int speed, long requiredPulsesforRotation) {         // function that will rotate the motor clockwise
  long targetEncoderValue = encoderValue + requiredPulsesforRotation;
  
  while (encoderValue <= targetEncoderValue) {
    analogWrite(enablePin, speed);
    digitalWrite(int1Pin, HIGH);
    digitalWrite(int2Pin, LOW);
    Serial.println(encoderValue);
  }
  stopMotor();  // stop after the motor completes the loop
  Serial.println("Motor has been stopped ");
}

void backward(int speed, long requiredPulsesforRotation) {        //function that will rotate the motor anticlockwise
  long targetEncoderValue = encoderValue - requiredPulsesforRotation;
  
  while (encoderValue >= targetEncoderValue) {
    analogWrite(enablePin, speed);
    digitalWrite(int1Pin, LOW);
    digitalWrite(int2Pin, HIGH);
    Serial.println("motor running in CCW Direction \n");
    Serial.println(encoderValue);
  }
  stopMotor();    //stop after the motor completes the loop
  Serial.println("Motor has been Stopped ");
}

void stopMotor() {          // function that will stop the motor
  digitalWrite(int1Pin, LOW);
  digitalWrite(int2Pin, LOW);
  Serial.println("motor stopped");
}

void directionCheck(long currentEncoderValue) {     //function to check rotation direction of the antenna
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

void requestStop(){       // software interrupt that will stop the motor at any point
  stopRequested = true;
  stopMotor();
}

void reset(long requiredPulsesForRotation) {                  // rotate the antenna to its reset position, which here is set to 0
  while (encoderValue >= 0) {
    analogWrite(enablePin,255);
    digitalWrite(int1Pin, LOW);
    digitalWrite(int2Pin, HIGH);
    Serial.println("!!RESETTING THE ANTENNA POSITIONS!!!");
  }
  stopMotor();
  Serial.println("Parameters reset. Antenna returned to original position.");
}
