import os 
import threading
import tkinter as tk
import time
import sys
import smbus 
from gpiozero import Button 
import i2cEncoderLibV2
import max31865
from simple_pid import PID
import atexit
from RPi import GPIO

# set working directory do script directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))


GPIO.setmode(GPIO.BCM)

bus=smbus.SMBus(1)


FontSize1=100
FontSize2=80
FontSize3=60

y1=50
y2=200
y3= 350
y4= 500

xHLT=35
xMLT=380
xBK= 730

xOffset = 20
xOffset2 = 40

# PT100 Calibration offset
HLT_Calib_offset = -0.7
MLT_Calib_offset = -0.5
BK_Calib_offset = -1.1


# Set wiring variable
HLT_pt100_cspin = 18
MLT_pt100_cspin = 19
BK_pt100_cspin = 26


HLT_heater_cspin=24 # or 24
BK_heater_cspin=23

HLT_encoder_cspin=0x10
BK_encoder_cspin=0x07



# Just for variables init
HLT_temp = 0
MLT_temp = 0
BK_temp = 0

HLT_temp_setpoint = 74
MLT_temp_setpoint = 74
BK_power_setpoint = 50


MLT_REGUL_MODE = False

BK_encoder = i2cEncoderLibV2.i2cEncoderLibV2(bus,BK_encoder_cspin)

while True :
    BK_encoder.updateStatus()
    if (BK_encoder.readStatus(i2cEncoderLibV2.PUSHP) and (BK_encoder.readStatus(i2cEncoderLibV2.PUSHR)==false)) : 
        print("Long push!")

    if ( BK_encoder.readStatus(i2cEncoderLibV2.PUSHP) and BK_encoder.readStatus(i2cEncoderLibV2.PUSHR)) :
        print("Fast push!")

    if ( BK_encoder.readStatus(i2cEncoderLibV2.PUSHD)) :
        print("Double push!")

    time.sleep(0.1)
