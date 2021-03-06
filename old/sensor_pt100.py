# -*- coding: utf-8 -*-
import max31865
import sys
import time
from global_settings import *
import paho.mqtt.client as mqtt
from brew_lib import *
NBsensorRead=5 #number of read for avearge measure

class PT100(object):
    # CONFIG PARAMETER & PROPERTIES
    csPin=0
    def __init__(self,csPinValue):
        csPin = csPinValue
    print ("csPin=" + str(csPin))
    RefRest = 430
    misoPin = 9
    mosiPin = 10
    clkPin = 11
    config = "0xA2" #ConfigText = Property.Select("Conversion Mode & Wires", options=["[0xB2] - 3 Wires Manual","[0xD2] - 3 Wires Auto","[0xA2] - 2 or 4 Wires Manual","[0xC2] - 2 or 4 Wires Auto"], description="Choose beetween 2, 3 or 4 wire PT100 & the Conversion mode at 60 Hz beetween Manual or Continuous Auto")
		#
		# Config Register
		# ---------------
		# bit 7: Vbias -> 1 (ON), 0 (OFF)
		# bit 6: Conversion Mode -> 0 (MANUAL), 1 (AUTO) !!don't change the noch fequency 60Hz when auto
		# bit5: 1-shot ->1 (ON)
		# bit4: 3-wire select -> 1 (3 wires config), 0 (2 or 4 wires)
		# bits 3-2: fault detection cycle -> 0 (none)
		# bit 1: fault status clear -> 1 (clear any fault)
		# bit 0: 50/60 Hz filter select -> 0 (60Hz - Faster converson), 1 (50Hz)
		#
		# 0b10110010 = 0xB2     (Manual conversion, 3 wires at 60Hz)
		# 0b10100010 = 0xA2     (Manual conversion, 2 or 4 wires at 60Hz)
		# 0b11010010 = 0xD2     (Continuous auto conversion, 3 wires at 60 Hz) 
		# 0b11000010 = 0xC2     (Continuous auto conversion, 2 or 4 wires at 60 Hz) 
		#

    def init(self):

        # INIT SENSOR
        self.ConfigReg = self.config
        self.max = max31865.max31865(int(self.csPin),int(self.misoPin), int(self.mosiPin), int(self.clkPin), int(self.RefRest), int(self.ConfigReg,16))

    def read(self):
        return round(self.max.readTemp(), 2)


sensorName=sys.argv[1]
csPinValue=sys.argv[2]
print ("Sensor PT100 Name :" + sensorName)
print("MQTT_Brocker:" + mqtt_brocker)
sensor=PT100(csPinValue=csPinValue)
sensor.init()


while 1:
	sensor_value= str(sensor.read())
	print("Temperature:" + sensor_value)
	json_msg={"sender":sensorName, "senderType":"sensor","dest"=controllerName,"valueName":"temeprature","value":sensor_value}
	send_msg (mqtt_brocker,topic,json_msg)
	time.sleep(1)
    
