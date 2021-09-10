#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

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
c = input("Do you calibration : Yes(y) or No(n):")
if c == "y":
	print("starting calibration...")
	my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	while my_drive.axis0.current_state != AXIS_STATE_IDLE:
		time.sleep(0.1)
	my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	time.sleep(0.1)
	my_drive.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
	


# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

# Or to change a value, just assign to the property
# my_drive.axis0.controller.input_torque = 0.1



my_drive.axis0.controller.input_pos = 0
time.sleep(3)
p0 = my_drive.axis0.encoder.pos_estimate
print("initial position is : " + str(p0))
my_drive.axis0.controller.input_pos = p0
time.sleep(3)


fq = 0.1 # 0.1 [Hz]
c = input("Please push Enter for starting test!!")
#with open('load_test_0126.csv', 'a',newline = '') as f:
	#w = csv.writer(f,delimiter=",")
t0 = time.perf_counter() # uint is ns
while True:
	setpoint = 2.0 * math.sin((time.perf_counter()-t0) * fq * 6.28318530718) # Amp. = 2 ±90 [deg.]
	my_drive.axis0.controller.input_pos = setpoint
	#p = my_drive.axis0.encoder.pos_estimate
	t = time.perf_counter()-t0
	until = time.perf_counter() + 0.01
	while time.perf_counter() < until:
		pass
	#if t > 3600: # t [sec.] : End time is 60*60 = 3600 [sec.]
		#break
		#if t % 5 == 0:	
			#w.writerow([t, setpoint,p])
time.sleep(5)
# my_drive.axis0.controller.input_pos= 0
