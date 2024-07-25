#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 14:15:34 2024

@author: madhav
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox, QGridLayout, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QFont, QColor, QPalette
import serial
import datetime
import time

# Define the file path for saving motor settings
file_path = 'motor_settings.txt'

class MotorControlGUI(QMainWindow):
    def __init__(self, motor_control):
        super().__init__()
        self.motor_control = motor_control
        self.initUI()
        
        #initialize serial communication
        self.init_serial()
        
    def init_serial(self):
        self.serial_port = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust COM port as needed

    def send_serial_command(self, command):
        if self.serial_port.is_open:
            self.serial_port.write(command.encode())
        else:
            QMessageBox.critical(self, "Serial Port Error", "Serial port is not open.")

    def initUI(self):
        self.setWindowTitle('Arduino Motor Control')
        self.setGeometry(100, 100, 800, 600)
        
        # Set dark mode theme
        self.setDarkMode()
    
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()  # Use QVBoxLayout for vertical layout
        central_widget.setLayout(main_layout)
    
        # First Row: Set Pulses per Revolution, Set Gear Ratio, Set Antenna Angle, Set Clock For Rotation
        first_row_layout = QHBoxLayout()
        main_layout.addLayout(first_row_layout)
    
        # Set Pulses per Revolution
        pulses_group = QGroupBox('Set Pulses per Revolution')
        pulses_layout = QVBoxLayout()
        pulses_group.setLayout(pulses_layout)
    
        self.pulses_entry = QLineEdit()
        pulses_layout.addWidget(self.pulses_entry)
    
        self.submit_pulses_button = QPushButton('Submit Pulses')
        self.submit_pulses_button.clicked.connect(self.submit_pulses)
        pulses_layout.addWidget(self.submit_pulses_button)
    
        first_row_layout.addWidget(pulses_group)
    
        # Set Gear Ratio
        gear_ratio_group = QGroupBox('Set Gear Ratio')
        gear_ratio_layout = QVBoxLayout()
        gear_ratio_group.setLayout(gear_ratio_layout)
    
        self.gear_ratio_entry = QLineEdit()
        gear_ratio_layout.addWidget(self.gear_ratio_entry)
    
        self.submit_gear_ratio_button = QPushButton('Submit Gear Ratio')
        self.submit_gear_ratio_button.clicked.connect(self.submit_gear_ratio)
        gear_ratio_layout.addWidget(self.submit_gear_ratio_button)
    
        first_row_layout.addWidget(gear_ratio_group)
    
        # Set Antenna Angle
        pulse_group = QGroupBox('Set Antenna Angle')
        pulse_layout = QVBoxLayout()
        pulse_group.setLayout(pulse_layout)
    
        pulse_label = QLabel('Enter Angle In Degrees:')
        pulse_layout.addWidget(pulse_label)
    
        self.pulse_entry = QLineEdit()
        pulse_layout.addWidget(self.pulse_entry)
    
        self.submit_angle_button = QPushButton('Submit Angle')
        self.submit_angle_button.clicked.connect(self.submit_angle)
        pulse_layout.addWidget(self.submit_angle_button)
        
        first_row_layout.addWidget(pulse_group)
    
        # Set Clock For Rotation
        timer_group = QGroupBox('Set Clock For Rotation')
        timer_layout = QVBoxLayout()
        timer_group.setLayout(timer_layout)
    
        self.hours_entry = QLineEdit('00')
        timer_layout.addWidget(self.hours_entry)
    
        self.minutes_entry = QLineEdit('00')
        timer_layout.addWidget(self.minutes_entry)
    
        self.seconds_entry = QLineEdit('00')
        timer_layout.addWidget(self.seconds_entry)
    
        start_stop_layout = QHBoxLayout()
        timer_layout.addLayout(start_stop_layout)
    
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_timer)
        start_stop_layout.addWidget(self.start_button)
    
        self.stop_button_timer = QPushButton('Stop')
        self.stop_button_timer.clicked.connect(self.stop_timer)
        start_stop_layout.addWidget(self.stop_button_timer)
    
        first_row_layout.addWidget(timer_group)

        # Second Row: Direction Controls, Speed Controls, Encoder Value
        second_row_layout = QHBoxLayout()
        main_layout.addLayout(second_row_layout)

        # Direction Controls
        direction_group = QGroupBox('Direction Controls')
        direction_layout = QVBoxLayout()
        direction_group.setLayout(direction_layout)
    
        self.forward_button = QPushButton('Clockwise')
        self.forward_button.clicked.connect(self.forward)
        direction_layout.addWidget(self.forward_button)
    
        self.backward_button = QPushButton('Anticlockwise')
        self.backward_button.clicked.connect(self.backward)
        direction_layout.addWidget(self.backward_button)
    
        self.direction_button = QPushButton('Direction Find')
        self.direction_button.clicked.connect(self.direction_count)
        direction_layout.addWidget(self.direction_button)
    
        second_row_layout.addWidget(direction_group)
    
        # Speed Controls
        motor_controls_group = QGroupBox('Speed Controls')
        motor_controls_layout = QVBoxLayout()
        motor_controls_group.setLayout(motor_controls_layout)
    
        self.speed_label = QLabel('Calculated Speed (PWM 0-255):')
        motor_controls_layout.addWidget(self.speed_label)
    
        self.calculated_speed_display = QLabel('N/A')
        motor_controls_layout.addWidget(self.calculated_speed_display)
    
        second_row_layout.addWidget(motor_controls_group)
    
        # Encoder Value
        encoder_group = QGroupBox('Encoder Value')
        encoder_layout = QVBoxLayout()
        encoder_group.setLayout(encoder_layout)
    
        self.encoder_value_label = QLabel('Current Encoder Value: N/A')
        encoder_layout.addWidget(self.encoder_value_label)
    
        self.read_encoder_button = QPushButton('Read Encoder Value')
        self.read_encoder_button.clicked.connect(self.read_encoder)
        encoder_layout.addWidget(self.read_encoder_button)
    
        second_row_layout.addWidget(encoder_group)

        # Third Row: Submit Parameters, Reset Parameters, Reset Antenna Position
        third_row_layout = QHBoxLayout()
        main_layout.addLayout(third_row_layout)
    
        self.submit_button = QPushButton('Submit Parameters')
        self.submit_button.clicked.connect(self.submit_parameters)
        third_row_layout.addWidget(self.submit_button)
    
        self.reset_button = QPushButton('Reset Parameters')
        self.reset_button.clicked.connect(self.reset_all)
        third_row_layout.addWidget(self.reset_button)
    
        self.reset_antenna_button = QPushButton('Reset Antenna Position')
        self.reset_antenna_button.clicked.connect(self.reset_antenna_position)
        third_row_layout.addWidget(self.reset_antenna_button)

        # Spacer
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        # Initialize settings from file
        self.read_motor_settings()

    def reset_antenna_position(self):
        self.pulse_entry.clear()
        self.send_serial_command('R')
        QMessageBox.information(self, "Reset Antenna Position", "Antenna position has been reset.")
        self.motor_control.write_log("Antenna position reset")

    def read_motor_settings(self):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    self.pulse_entry.setText(lines[1].strip())

    def start_timer(self):
        try:
            # Convert user input for hours, minutes, and seconds into total seconds
            total_time = int(self.hours_entry.text()) * 3600 + int(self.minutes_entry.text()) * 60 + int(self.seconds_entry.text())
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Please enter valid integers for hours, minutes, and seconds.")
            return

        # Ensure total_time is not zero to avoid division by zero
        if total_time == 0:
            QMessageBox.critical(self, "Invalid Input", "Total time must be greater than zero.")
            return
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        # Calculate the time in minutes from the total time in seconds
        time_in_minutes = total_time / 60
        
        # Fetch the angle entered by the user in the GUI
        angle = self.pulse_entry.text().strip()
        try:
            angle_value = float(angle)
            if angle_value < 0 or angle_value > 360:
                raise ValueError("Angle must be between 0 and 360 degrees.")
            
            # Calculate the angle per minute
            angle_per_minute = angle_value / time_in_minutes

            # Calculate PWM for the given angle per minute
            max_pwm = 255
            pwm_value = min(max(int((angle_per_minute * max_pwm) / 360), 0), max_pwm)

            # Display calculated PWM in the GUI
            self.calculated_speed_display.setText(str(pwm_value))

            # Log the PWM value to file
            self.motor_control.write_log(f"Timer set: {total_time} seconds, Angle: {angle_value} degrees, Angle per minute: {angle_per_minute}, PWM calculated: {pwm_value}")

            # Send the PWM value to Arduino via serial
            self.send_serial_command(f"P{pwm_value}")

            # Debug print to console
            print(f"Timer set: {total_time} seconds, Angle: {angle_value} degrees, Angle per minute: {angle_per_minute}, PWM calculated: {pwm_value}")

        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", str(e))

    # Method to send PWM value to Arduino
    def send_pwm_to_arduino(self, pwm_value):
        if self.arduino_serial.isOpen():
            self.arduino_serial.write(f"{pwm_value}\n".encode())
        else:
                print("Serial connection to Arduino is not open.")


    def stop_timer(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.motor_control.stop_motor()
        QMessageBox.information(self, "Timer Stopped", "The timer has been stopped and motor has been stopped.")
        self.motor_control.write_log("Timer stopped")

    @pyqtSlot()
    def update_timer(self):
        total_time = int(self.hours_entry.text()) * 3600 + int(self.minutes_entry.text()) * 60 + int(self.seconds_entry.text())
        total_time -= 1

        hours = total_time // 3600
        minutes = (total_time % 3600) // 60
        seconds = total_time % 60

        self.hours_entry.setText(f"{hours:02}")
        self.minutes_entry.setText(f"{minutes:02}")
        self.seconds_entry.setText(f"{seconds:02}")

        if total_time <= 0:
            self.timer.stop()
            self.motor_control.stop_motor()
            QMessageBox.information(self, "Timer Finished", "The timer has finished and motor has been stopped.")
            self.motor_control.write_log("Timer finished")
   
    def submit_parameters(self):
        angle = self.pulse_entry.text()
        self.motor_control.send_command(f"A{angle}")

        # Handle pulses per revolution separately if needed
        pulses_per_revolution = self.pulses_entry.text()
        if pulses_per_revolution.isdigit():
            self.motor_control.set_pulses_per_revolution(int(pulses_per_revolution))

        self.motor_control.write_motor_settings()
        QMessageBox.information(self, "Parameters Set", "All parameters have been submitted and set.")
        self.motor_control.write_log(f"Angle set: {angle}, Pulses per revolution set: {pulses_per_revolution}")

    def submit_angle(self):
        angle = self.pulse_entry.text().strip()
        try:
            angle_value = int(angle)
            if angle_value < 0 or angle_value > 360:
                raise ValueError("Angle must be between 0 and 360 degrees.")

            # Send angle value to Arduino
            self.send_serial_command(f"A{angle_value}")
            QMessageBox.information(self, "Angle Set", f"Angle set to {angle_value} degrees.")
            self.motor_control.write_log(f"Angle set: {angle_value}")

        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", str(e))
    
    def submit_pulses(self):
        pulses_per_revolution = self.pulses_entry.text().strip()
        try:
            pulses_value = int(pulses_per_revolution)
            if pulses_value <= 0:
                raise ValueError("Pulses per revolution must be a positive integer.")

            # Send pulses per revolution value to Arduino
            self.send_serial_command(f"P{pulses_value}")
            QMessageBox.information(self, "Pulses Set", f"Pulses per revolution set to {pulses_value}.")
            self.motor_control.write_log(f"Pulses per revolution set: {pulses_value}")

        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", str(e))
    
    def submit_gear_ratio(self):
        gear_ratio_text = self.gear_ratio_entry.text().strip()
        try:
            gear_ratio = float(gear_ratio_text)
            if gear_ratio <= 0:
                raise ValueError("Gear ratio must be a positive number.")

            # Send gear ratio value to Arduino
            self.send_serial_command(f"G{gear_ratio}")
            QMessageBox.information(self, "Gear Ratio Set", f"Gear ratio set to {gear_ratio}.")
            self.motor_control.write_log(f"Gear ratio set: {gear_ratio}")

        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", str(e))


    def forward(self):
        self.send_serial_command('F')  # Send command 'F' for forward to Arduino
        QMessageBox.information(self, "Direction Set", "Direction set to Clockwise")
        self.motor_control.write_log("Direction set to Clockwise")

    def backward(self):
        self.send_serial_command('B')  # Send command 'B' for backward to Arduino
        QMessageBox.information(self, "Direction Set", "Direction set to Anticlockwise")
        self.motor_control.write_log("Direction set to Anticlockwise")

    def direction_count(self):
        self.send_serial_command('D')  # Send command 'D' for direction count to Arduino
        QMessageBox.information(self, "Direction Count", "Direction count set")
        self.motor_control.write_log("Direction count set")

    def read_encoder(self):
        self.send_serial_command('E')  # Send command 'E' to request encoder value
        time.sleep(0.1)  # Wait for the Arduino to process and respond

        if self.serial_port.in_waiting > 0:
                encoder_value = self.serial_port.readline().decode().strip()
                self.encoder_value_label.setText(f"Current Encoder Value: {encoder_value}")
                self.motor_control.write_log(f"Encoder value read: {encoder_value}")
        else:
                QMessageBox.critical(self, "Read Error", "Failed to read encoder value. No data available.")
                self.motor_control.write_log("Failed to read encoder value")

    def reset_all(self):
        self.pulse_entry.clear()
        self.hours_entry.setText('00')
        self.minutes_entry.setText('00')
        self.seconds_entry.setText('00')
        self.calculated_speed_display.setText('N/A')
        self.encoder_value_label.setText('Current Encoder Value: N/A')
        self.motor_control.stop_motor()
        QMessageBox.information(self, "Reset", "All settings have been reset.")
        self.motor_control.write_log("All settings reset")

    def setDarkMode(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

    def closeEvent(self, event):
        self.serial_port.close()
        super().closeEvent(event)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    motor_control = None  # Replace with your motor control instance
    window = MotorControlGUI(motor_control)
    window.show()
    sys.exit(app.exec_())
