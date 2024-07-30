#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 12:30:10 2024

@author: madhav
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
        self.setFixedSize(800, 300)
        self.setDarkMode()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # First Row: Set Pulses per Revolution, Set Gear Ratio, Set Antenna Angle, Set Clock For Rotation
        first_row_layout = QHBoxLayout()
        main_layout.addLayout(first_row_layout)

        # Set Pulses per Revolution
        pulses_group = QGroupBox('ENCODER SETTINGS')
        pulses_group.setStyleSheet("""
                                   QGroupBox {
                                       font-weight: bold;
                                       font-size: 13px;
                                       }
                                   """)
        pulses_layout = QVBoxLayout()
        pulses_group.setLayout(pulses_layout)
        
        # Add bold and larger font label
        pulses_title_label = QLabel('Pulses Per Revolution of Encoder')
        pulses_layout.addWidget(pulses_title_label)
        
        self.pulses_entry = QLineEdit()
        pulses_layout.addWidget(self.pulses_entry)
        
        self.submit_pulses_button = QPushButton('Submit Pulses')
        self.submit_pulses_button.clicked.connect(self.submit_pulses)
        pulses_layout.addWidget(self.submit_pulses_button)
        
        first_row_layout.addWidget(pulses_group)

        # Set Gear Ratio
        gear_ratio_group = QGroupBox('Set Gear Ratio')
        gear_ratio_group.setStyleSheet("""
                                   QGroupBox {
                                       font-weight: bold;
                                       font-size: 13px;
                                       }
                                   """)
        gear_ratio_layout = QVBoxLayout()
        gear_ratio_group.setLayout(gear_ratio_layout)
        
        # Add bold and larger font label
        gear_ratio_title_label = QLabel('ANTENNA RATIO')
        gear_ratio_layout.addWidget(gear_ratio_title_label)
        
        self.gear_ratio_entry = QLineEdit()
        gear_ratio_layout.addWidget(self.gear_ratio_entry)
        
        self.submit_gear_ratio_button = QPushButton('Submit Gear Ratio')
        self.submit_gear_ratio_button.clicked.connect(self.submit_gear_ratio)
        gear_ratio_layout.addWidget(self.submit_gear_ratio_button)
        
        first_row_layout.addWidget(gear_ratio_group)

        # Set Antenna Angle
        pulse_group = QGroupBox('Set Antenna Angle')
        pulse_group.setStyleSheet("""
                                   QGroupBox {
                                       font-weight: bold;
                                       font-size: 13px;
                                       }
                                   """)
        pulse_layout = QVBoxLayout()
        pulse_group.setLayout(pulse_layout)
        
        # Add bold and larger font label
        pulse_title_label = QLabel('ROTATION ANGLE')
        pulse_layout.addWidget(pulse_title_label)
        
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
        timer_group.setStyleSheet("""
                                   QGroupBox {
                                       font-weight: bold;
                                       font-size: 13px;
                                       }
                                   """)
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
        direction_group.setStyleSheet("""
                                   QGroupBox {
                                       font-weight: bold;
                                       font-size: 13px;
                                       }
                                   """)
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
        motor_controls_group.setStyleSheet("""
                                   QGroupBox {
                                       font-weight: bold;
                                       font-size: 13px;
                                       }
                                   """)
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
        encoder_group.setStyleSheet("""
                                   QGroupBox {
                                       font-weight: bold;
                                       font-size: 13px;
                                       }
                                   """)
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
            self.pwm_value = int((angle_per_minute / 360) * max_pwm)
            self.calculated_speed_display.setText(f'{self.pwm_value}')
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", f"Please enter a valid angle between 0 and 360 degrees.\nError: {e}")
            return

    def stop_timer(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
            self.send_serial_command('S')
            QMessageBox.information(self, "Timer Stopped", "The timer has been stopped.")
        else:
            QMessageBox.warning(self, "No Timer", "No timer is running.")

    def set_speed(self):
        if self.pwm_value is not None:
            self.send_serial_command(f'S{self.pwm_value}')
            QMessageBox.information(self, "Speed Set", f"Speed set to PWM value: {self.pwm_value}")
        else:
            QMessageBox.warning(self, "No Speed Calculated", "Speed has not been calculated yet.")

    def forward(self):
        self.send_serial_command('F')
        QMessageBox.information(self, "Direction", "Motor is set to move clockwise.")
        self.motor_control.write_log("Motor set to move clockwise")

    def backward(self):
        self.send_serial_command('B')
        QMessageBox.information(self, "Direction", "Motor is set to move anticlockwise.")
        self.motor_control.write_log("Motor set to move anticlockwise")

    def direction_count(self):
        self.send_serial_command('D')
        QMessageBox.information(self, "Direction Count", "Direction count command sent.")
        self.motor_control.write_log("Direction count command sent")

    def submit_pulses(self):
        pulses = self.pulses_entry.text().strip()
        try:
            pulses_value = int(pulses)
            if pulses_value <= 0:
                raise ValueError("Pulses per revolution must be a positive integer.")
            self.send_serial_command(f'P{pulses_value}')
            QMessageBox.information(self, "Pulses Set", f"Pulses per revolution set to: {pulses_value}")
            self.motor_control.write_log(f"Pulses per revolution set to: {pulses_value}")
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", f"Please enter a valid positive integer for pulses per revolution.\nError: {e}")

    def submit_gear_ratio(self):
        gear_ratio = self.gear_ratio_entry.text().strip()
        try:
            gear_ratio_value = float(gear_ratio)
            if gear_ratio_value <= 0:
                raise ValueError("Gear ratio must be a positive number.")
            self.send_serial_command(f'G{gear_ratio_value}')
            QMessageBox.information(self, "Gear Ratio Set", f"Gear ratio set to: {gear_ratio_value}")
            self.motor_control.write_log(f"Gear ratio set to: {gear_ratio_value}")
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", f"Please enter a valid positive number for gear ratio.\nError: {e}")

    def submit_angle(self):
        angle = self.pulse_entry.text().strip()
        try:
            angle_value = float(angle)
            if angle_value < 0 or angle_value > 360:
                raise ValueError("Angle must be between 0 and 360 degrees.")
            self.send_serial_command(f'A{angle_value}')
            QMessageBox.information(self, "Angle Set", f"Angle set to: {angle_value} degrees")
            self.motor_control.write_log(f"Angle set to: {angle_value} degrees")
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", f"Please enter a valid angle between 0 and 360 degrees.\nError: {e}")

    def submit_parameters(self):
        pulses = self.pulses_entry.text().strip()
        gear_ratio = self.gear_ratio_entry.text().strip()
        angle = self.pulse_entry.text().strip()
        try:
            pulses_value = int(pulses)
            gear_ratio_value = float(gear_ratio)
            angle_value = float(angle)
            if pulses_value <= 0 or gear_ratio_value <= 0 or angle_value < 0 or angle_value > 360:
                raise ValueError("Invalid parameters.")
            self.send_serial_command(f'P{pulses_value}G{gear_ratio_value}A{angle_value}')
            QMessageBox.information(self, "Parameters Submitted", "All parameters have been submitted.")
            self.motor_control.write_log(f"Parameters submitted: Pulses per revolution={pulses_value}, Gear ratio={gear_ratio_value}, Angle={angle_value}")
        except ValueError as e:
            QMessageBox.critical(self, "Invalid Input", f"Please enter valid parameters.\nError: {e}")

    def reset_all(self):
        self.pulses_entry.clear()
        self.gear_ratio_entry.clear()
        self.pulse_entry.clear()
        QMessageBox.information(self, "Parameters Reset", "All parameters have been reset.")
        self.motor_control.write_log("All parameters have been reset")

    def read_encoder(self):
        self.send_serial_command('E')
        # Update this with actual encoder reading logic if needed
        QMessageBox.information(self, "Encoder Read", "Encoder reading command sent.")

    def setDarkMode(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

        self.setPalette(dark_palette)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    motor_control = None  # Replace with actual motor control instance
    main_window = MotorControlGUI(motor_control)
    main_window.show()
    sys.exit(app.exec_())
