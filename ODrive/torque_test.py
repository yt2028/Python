#!/usr/bin/env python3
from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math
import csv
# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
# my_drive = odrive.find_any("serial:/dev/ttyUSB0")

# Calibrate motor and wait for it to finish
c = input("Do you calibrate : Yes(y) or No(n):")
if c == "y":
	print("starting calibration...")
	my_drive.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	while my_drive.axis1.current_state != AXIS_STATE_IDLE:
		time.sleep(0.1)
	my_drive.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	time.sleep(0.1)
	my_drive.axis1.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
	print('CONTROL MODE : POSITION')
	


# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

# Or to change a value, just assign to the property
# my_drive.axis1.controller.input_torque = 0.1



my_drive.axis1.controller.input_pos = 0
time.sleep(3)
p0 = my_drive.axis1.encoder.pos_estimate
print("initial position is : " + str(p0))
my_drive.axis1.controller.input_pos = p0
time.sleep(3)


fq = 0.05 # [Hz]
print("Freq. = 0.1 Hz, Range = 90 deg.")
#d = input("Please set rotate direction :CW(c) or CCW(w):") 
c = input("Please push Enter for starting test!!")
t0 = time.perf_counter() 

while True:
    setpoint = 7.5 * math.sin((time.perf_counter()-t0) * fq * 6.28318530718) 
    my_drive.axis1.controller.input_pos = setpoint
    p = my_drive.axis1.encoder.pos_estimate
    t = time.perf_counter()-t0
    until = time.perf_counter() + 0.01
    while time.perf_counter() < until:
        pass
    if setpoint > 7.49:
        break

