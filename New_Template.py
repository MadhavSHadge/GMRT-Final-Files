#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 09:35:27 2024
@author: Madhav Hadge
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QGroupBox, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor
import serial
import datetime

# Define the file path for saving motor settings
file_path = '/home/madhav/Documents/FINALS/IMPROVED FROM GUI_VERSION_7/motor_settings.txt'

class MotorControlGUI(QMainWindow):
    def __init__(self, motor_control):
        super().__init__()
        self.motor_control = motor_control
        self.pwm_value = None  # Initialize PWM value as None
        self.initUI()
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
        self.setDarkMode()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
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
    
        # Speed Set Button
        self.speed_set_button = QPushButton('Speed Set')
        self.speed_set_button.clicked.connect(self.set_speed)
        motor_controls_layout.addWidget(self.speed_set_button)
    
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
            total_time = int(self.hours_entry.text()) * 3600 + int(self.minutes_entry.text()) * 60 + int(self.seconds_entry.text())
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Please enter valid integers for hours, minutes, and seconds.")
            return

        if total_time == 0:
            QMessageBox.critical(self, "Invalid Input", "Total time must be greater than zero.")
            return
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        time_in_minutes = total_time / 60
        
        angle = self.pulse_entry.text().strip()
        try:
            angle_value = float(angle)
            if angle_value < 0 or angle_value > 360:
                raise ValueError("Angle must be between 0 and 360 degrees.")
            
            angle_per_minute = angle_value / time_in_minutes
            max_pwm = 255
            self.pwm_value = min(max(int((angle_per_minute * max_pwm) / 360), 0), max_pwm)

            self.calculated_speed_display.setText(str(self.pwm_value))
            self.motor_control.write_log(f"Timer set: {total_time} seconds, Angle: {angle_value} degrees, Angle per minute: {angle_per_minute}, PWM calculated: {self.pwm_value}")

            self.send_serial_command(f"PWM:{self.pwm_value}")

        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", str(e))
    
    def update_timer(self):
        try:
            hours = int(self.hours_entry.text())
            minutes = int(self.minutes_entry.text())
            seconds = int(self.seconds_entry.text())

            if seconds > 0:
                seconds -= 1
            elif minutes > 0:
                minutes -= 1
                seconds = 59
            elif hours > 0:
                hours -= 1
                minutes = 59
                seconds = 59
            else:
                self.stop_timer()
                QMessageBox.information(self, "Timer Finished", "The timer has finished.")
                return

            self.hours_entry.setText(str(hours).zfill(2))
            self.minutes_entry.setText(str(minutes).zfill(2))
            self.seconds_entry.setText(str(seconds).zfill(2))
        except ValueError:
            QMessageBox.critical(self, "Invalid Input", "Please enter valid integers for hours, minutes, and seconds.")
            self.timer.stop()

    def stop_timer(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
            self.send_serial_command('S')
            self.motor_control.write_log("Timer stopped and 'S' command sent to Arduino")

    def submit_pulses(self):
        pulses_per_rev = self.pulses_entry.text().strip()
        self.send_serial_command(f"P:{pulses_per_rev}")

    def submit_gear_ratio(self):
        gear_ratio = self.gear_ratio_entry.text().strip()
        self.send_serial_command(f"G:{gear_ratio}")

    def submit_angle(self):
        angle = self.pulse_entry.text().strip()
        self.send_serial_command(f"A:{angle}")

    def set_speed(self):
        try:
            if self.pwm_value is None:
                QMessageBox.critical(self, "Invalid Speed", "Calculated speed is not available.")
                return

            if not (0 <= self.pwm_value <= 255):
                raise ValueError("Speed value must be between 0 and 255.")
            
            self.send_serial_command(f"M{self.pwm_value}")
            QMessageBox.information(self, "Speed Set", f"Speed set to {self.pwm_value}")
            self.motor_control.write_log(f"Speed set to {self.pwm_value}")

        except ValueError as e:
            QMessageBox.critical(self, "Invalid Speed", str(e))

    def submit_parameters(self):
        self.start_timer()
        pulses_per_rev = self.pulses_entry.text().strip()
        gear_ratio = self.gear_ratio_entry.text().strip()
        angle = self.pulse_entry.text().strip()

        with open(file_path, 'w') as file:
            file.write(f"{pulses_per_rev}\n")
            file.write(f"{angle}\n")
        
        self.motor_control.write_log(f"Parameters submitted: Pulses per Rev: {pulses_per_rev}, Gear Ratio: {gear_ratio}, Antenna Angle: {angle}")

    def reset_all(self):
        self.pulses_entry.clear()
        self.gear_ratio_entry.clear()
        self.pulse_entry.clear()
        self.hours_entry.setText('00')
        self.minutes_entry.setText('00')
        self.seconds_entry.setText('00')
        self.calculated_speed_display.setText('N/A')
        self.send_serial_command('Reset')
        QMessageBox.information(self, "Reset", "All parameters have been reset.")

    def forward(self):
        self.send_serial_command('F')
        self.motor_control.write_log("Motor set to rotate clockwise")

    def backward(self):
        self.send_serial_command('B')
        self.motor_control.write_log("Motor set to rotate anticlockwise")

    def direction_count(self):
        self.send_serial_command('D')
        self.motor_control.write_log("Direction find initiated")

    def read_encoder(self):
        self.send_serial_command('RE')
        self.motor_control.write_log("Read encoder value command sent")

    def setDarkMode(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        self.setPalette(dark_palette)

class MotorControl:
    def __init__(self):
        log_folder = "motor_logs"
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
        log_filename = f"{log_folder}/motor_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.log_file = open(log_filename, "w")
    
    def write_log(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_file.write(f"{timestamp}: {message}\n")
        self.log_file.flush()

    def close(self):
        self.log_file.close()

if __name__ == '__main__':
    motor_control = MotorControl()
    app = QApplication(sys.argv)
    window = MotorControlGUI(motor_control)
    window.show()
    app.exec_()
    motor_control.close()
