# README

## Arduino Motor Control with Encoder Feedback

This Arduino sketch is designed to control a motor with an encoder for precise positioning. The system includes functions to set the motor speed, direction, and position based on encoder feedback. 
It communicates with a host computer via Serial, allowing for commands to be sent from a Python GUI.

### Hardware Setup

- **Motor Driver Pins:**
  - `enablePin`: Pin 9 (PWM for motor speed control)
  - `int1Pin`: Pin 8 (Motor driver input 1)
  - `int2Pin`: Pin 7 (Motor driver input 2)
- **Encoder Pins:**
  - `encoderPin1`: Pin 2
  - `encoderPin2`: Pin 3

### Variables

- `encoderValue`: Keeps track of the current position of the encoder.
- `pulsesPerRevolution`: Encoder value for pulses per revolution.
- `maximumEncoderValue`: Maximum encoder value for a full 360-degree rotation.
- `requiredPulsesForRotation`: Pulses required for a specific rotation.
- `gearRatio`: Gear ratio of the motor (default is 1).
- `antennaAngle`: Desired angle for the antenna.
- `newPulses`: New pulses per revolution value from the serial input.
- `speed`: Motor speed value from the serial input.
- `stopRequested`: Boolean flag to stop the motor.

### Functions

- `setup()`: Initializes the serial communication, sets pin modes, and attaches interrupts for the encoder.
- `loop()`: Reads serial commands and processes them.
- `conversion()`: Converts pulses to the maximum encoder value and calculates required pulses for rotation.
- `updateEncoder()`: Interrupt service routine to update encoder value.
- `forward()`: Rotates the motor clockwise to the target position.
- `backward()`: Rotates the motor counter-clockwise to the target position.
- `stopMotor()`: Stops the motor.
- `directionCheck()`: Checks the rotation direction of the antenna.
- `reset()`: Resets the antenna to the zero position.
- `requestStop()`: Software interrupt to stop the motor.

### Serial Commands

- `A`: Set antenna angle.
- `P`: Set pulse count per revolution.
- `G`: Set gear ratio.
- `F`: Rotate motor clockwise.
- `B`: Rotate motor counter-clockwise.
- `D`: Check direction of rotation.
- `R`: Reset antenna position to zero.
- `S`: Stop the motor.
- `M`: Set motor speed (PWM value).

### Example Usage

1. **Setting the Antenna Angle:**
   ```python
   serial.write(b'A')
   serial.write(b'45')  # Set angle to 45 degrees
   ```

2. **Setting the Pulse Count per Revolution:**
   ```python
   serial.write(b'P')
   serial.write(b'400')  # Set pulses per revolution to 400
   ```

3. **Setting the Gear Ratio:**
   ```python
   serial.write(b'G')
   serial.write(b'5')  # Set gear ratio to 5
   ```

4. **Rotating Motor Clockwise:**
   ```python
   serial.write(b'F')
   ```

5. **Rotating Motor Counter-Clockwise:**
   ```python
   serial.write(b'B')
   ```

6. **Checking Rotation Direction:**
   ```python
   serial.write(b'D')
   ```

7. **Resetting Antenna Position:**
   ```python
   serial.write(b'R')
   ```

8. **Stopping the Motor:**
   ```python
   serial.write(b'S')
   ```

9. **Setting Motor Speed:**
   ```python
   serial.write(b'M')
   serial.write(b'150')  # Set speed to 150
   ```

### Notes

- Ensure the encoder and motor driver are properly connected to the specified pins.
- The gear ratio and pulses per revolution must be correctly set to achieve accurate positioning.
- Use the `requestStop` function to safely stop the motor at any point during operation.

This setup and code allow for precise motor control, making it suitable for applications such as antenna positioning, requiring accurate rotational control.
