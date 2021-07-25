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
    my_drive.axis1.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
    print("CONTROL MODE : VELOCITY")
	


# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

# Or to change a value, just assign to the property
# my_drive.axis1.controller.input_torque = 0.1

while True:
    v = input("Please set velocity 0 - 100 rps : ")
    v = int(v)
    if v > 101:
        continue
    elif v <= 100:
        break

d = input("Please set rotate direction :CW(c) or CCW(w):") # [rps] max : 33 rpm (2000 rpm)
s = input("Please set save filename : ") # set file name
if d == 'c':
    my_drive.axis1.controller.input_vel = v # CW
else :
    my_drive.axis1.controller.input_vel = -1*v # CCW

for j in range(1,v+1):
    if d == 'c':
        my_drive.axis1.controller.input_vel = j
        time.sleep(0.1) # accel
    elif d == 'w':
        my_drive.axis1.controller.input_vel = -1*j
        time.sleep(0.1) # accel

t0 = time.perf_counter() # [ns]
with open(s +'.csv', 'a',newline = '') as f:
    w = csv.writer(f,delimiter=",")
    while True:
        t = time.perf_counter()-t0
        vm = my_drive.axis1.encoder.vel_estimate*60 # [rpm]
        i = my_drive.axis1.motor.current_control.Iq_measured* 0.0251 #my_drive.axis1.motor.config.torque_constant
        until = time.perf_counter() + 0.1
        while time.perf_counter() < until:
            pass	
        w.writerow([t, vm, i])
        if t > 10:
            for i in range(1,v+1):
                if d == 'c':
                    my_drive.axis1.controller.input_vel = v - i
                    time.sleep(0.1) # deaccel
                elif d == 'w':
                    my_drive.axis1.controller.input_vel = -1*v + i
                    time.sleep(0.1) # deaccel
            break
