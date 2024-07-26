# GMRT-Final-Files
---

# Arduino Motor Control GUI

This project provides a graphical user interface (GUI) for controlling a motor connected to an Arduino. The GUI is built using PyQt5 and allows the user to set various parameters, control the motor's direction and speed, and read encoder values. 

## Features

- **Set Pulses per Revolution:** Enter the number of pulses per revolution for the motor.
- **Set Gear Ratio:** Enter the gear ratio of the motor.
- **Set Antenna Angle:** Specify the angle for the antenna in degrees.
- **Set Clock for Rotation:** Specify the time duration for the motor rotation in hours, minutes, and seconds.
- **Direction Controls:** Control the direction of the motor (Clockwise, Anticlockwise, and Direction Find).
- **Speed Controls:** Set and display the motor speed in PWM values.
- **Encoder Value:** Read and display the current encoder value.
- **Submit Parameters:** Submit all set parameters to the motor.
- **Reset Parameters:** Reset all parameters to their default values.
- **Reset Antenna Position:** Reset the antenna position for calibration.
- **Dark Mode:** The GUI is designed with a dark mode theme for a better visual experience.

## Prerequisites

- Python 3.x
- PyQt5
- PySerial

You can install the required packages using pip:

```bash
pip install pyqt5 pyserial
```

## File Structure

- **motor_settings.txt:** File to save motor settings.
- **motor_logs:** Directory to save log files.
- **main.py:** Main script to run the GUI application.

## Usage

1. **Connect your Arduino:** Ensure your Arduino is connected to the correct serial port (e.g., `/dev/ttyUSB0` for Linux or `COMx` for Windows).

2. **Run the Application:**

    ```bash
    python main.py
    ```

3. **Set Parameters:** Use the GUI to set pulses per revolution, gear ratio, antenna angle, and rotation time.

4. **Control Motor:** Use the direction and speed controls to operate the motor.

5. **Submit and Save Parameters:** Submit all parameters to the Arduino and save them to the `motor_settings.txt` file.

6. **Reset Parameters:** Reset all parameters to default values.

7. **Log Files:** Check the `motor_logs` directory for log files containing details of all operations performed.

## Code Overview

### Main Classes

#### `MotorControlGUI(QMainWindow)`
- **initUI():** Initializes the user interface and layouts.
- **init_serial():** Initializes the serial communication with Arduino.
- **send_serial_command(command):** Sends a command to the Arduino via serial communication.
- **start_timer():** Starts the timer and calculates the motor speed in PWM.
- **update_timer():** Updates the timer every second.
- **stop_timer():** Stops the timer and the motor.
- **submit_pulses():** Submits the pulses per revolution to the Arduino.
- **submit_gear_ratio():** Submits the gear ratio to the Arduino.
- **submit_angle():** Submits the antenna angle to the Arduino.
- **set_speed():** Sets the motor speed in PWM.
- **submit_parameters():** Submits all parameters to the Arduino and saves them to the file.
- **reset_all():** Resets all parameters to their default values.
- **forward():** Sets the motor direction to clockwise.
- **backward():** Sets the motor direction to anticlockwise.
- **direction_count():** Finds the motor direction.
- **read_encoder():** Reads the encoder value from the Arduino.
- **setDarkMode():** Applies the dark mode theme to the GUI.

#### `MotorControl`
- **write_log(message):** Writes a log message to the log file.
- **close():** Closes the log file.
