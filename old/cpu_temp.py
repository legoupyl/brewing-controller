# -*- coding: utf-8 -*-
import sys
import time
import paho.mqtt.client as mqtt
import json


topic="xavfan/data"
mqtt_brocker="brocker.legoupyl.com"

def send_msg (mqtt_brocker,topic,json_msg):
	try:
		client = mqtt.Client()
		client.connect(mqtt_brocker,1883,60)
		client.publish(topic, str (json_msg))
		client.disconnect()
	except:
		pass


print("C'est parti pour la demo!!!")
print("Accrochez vous !")

while 1:
	f= open("/sys/class/thermal/thermal_zone0/temp","r")
	sensor_value= f.read()
	f.close()
	sensor_value = str (round (int (sensor_value) / 1000,1 ))
	print("Temperature CPU:" + sensor_value)
	json_msg={"deviceid": "neos", "temp_cpu": sensor_value }
	json_msg_str= json.dumps (json_msg)
	print (json_msg_str)
	send_msg (mqtt_brocker,topic,json_msg_str)
	time.sleep(1)
    
