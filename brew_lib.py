import sys
import threading
import time
import json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

class brewery:
	def __init__(self):
		self.name = "Goupyl's brewery"
		self.brocker ="brocker.legoupyl.com"
		self.controllerTopic = "controller"
		self.HLT = "HLT"
		self.MLT = "MLT"
		self.BT = "BT"

MyBrewery =  brewery ()

class sensor:
	def __init__(self, name,type, valueName):
		self.name = name
		self.type = "pt100"
		self.valueName = valueName
		self.value = -273
		self.msg =msg(name,"controller","measure")
	def start (self):
		self.thread = threading.Thread(target=self.run, args=())
		self.thread.daemon = True
		self.is_running = True
		self.thread.start()  
	def run(self):
		while self.is_running:
			self.value= 67
			self.msg.send (self.value)
			time.sleep (1)
	def stop(self):
		self.is_running = False


class controller:
	def __init__(self, name, type, sensor, actor):
		self.type = "tempController"
		self.name = name
		self.state = ""
		self.sensor = ""
		self.sensorValue= -273
		self.actor =""
		self.actorValue= 0
		self.actorConsigne = 0
		self.contollerSate = False
		self.consoleMsg =msg(self.name,"console","controllerState")
		self.actorMsg=msg(self.name,self.actor,"command")
		self.listner = listner(self,"controller")
	
	def on_message (self,json_msg):
		log ("Conroller MSG RCV", "ok")
		log ("debug" ,"self.sensor")
		log ("debug", self.sensor)
		if  json_msg ["sender"] == self.sensor:
			self.sensorValue=json_msg ["value"]
			log ("RcvSensorValue", self.sensorValue)
		if  json_msg ["sender"] == self.actor:
			self.actorValue= json_msg ["value"]
			log ("RcvActorValue", self.actorValue)
		if  json_msg ["recipient"] == self.name and  json_msg ["sender"] == "console":
			if  json_msg ["type"] == "actorConsigne":
				self.actorConsigne = json_msg ["value"]
				log ("RcvActorConsigne", self.actorValue)
			if  json_msg ["type"] == "contollerSate ":
				self.contollerSate = json_msg ["value"]
				log ("RcvControllerState", self.contollerSate)	
				self.consoleMsg.send (contollerSate)
				log ("SendCurrentControllerState", self.contollerSate)		
	def start ():
		self.run()
	def run ():
		while 1:
			time.sleep (10)


class listner (controller):
	def on_connect(self,client, userdata, flags, rc):
		log ("mqqt", "Connected with result code " + str(rc))
		client.subscribe("controller")

	def on_message(self,client, userdata, msg):
			mqtt_msg_str=msg.payload.decode()
			log ("MSG", "Received :" + mqtt_msg_str)
			json_msg=json.loads (mqtt_msg_str)
			log ("MSG", "Loaded JSON MSG" + mqtt_msg_str )
			try:
				super().on_message(json_msg)
			except Exception as e: print(e)
			

	def __init__(self,recipient):
		self.recipient= recipient # used to filter messages
		self.client = mqtt.Client()
		self.connected = False
		while not self.connected :
			log ("BrockerConnect",MyBrewery.brocker )
			self.client.connect(MyBrewery.brocker,1883,60)
			self.client.on_connect = self.on_connect
			self.client.on_message = self.on_message
			self.client.loop_start()
			self.connected = True
		self.client.loop_forever()




class actor:
	def __init__(self, name,gpio_num,freq):
		self.name = name
		self.gpio_num=gpio_num
		self.freq=freq
		self.gpio = gpio_pwm (self.gpio_num, self.freq)
		self.msg = msg (name,"controller","state")
		
	def on (self,power):
		self.gpio.start (power)
		self.msg.send (power)
	def off (self):
		self.gpio.stop ()
		self.msg.send (power)



class gpio_pwm ():
	def __init__(self,gpio_num,freq):
		self.freq = 1
		self.power = 0
		self._is_running=False
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.gpio_num, GPIO.OUT)

	def start (self):
		self.thread = threading.Thread(target=self.run, args=())
		self.thread.daemon = True
		self.is_running = True
		self.thread.start()  

	def run (self):
		while self.is_running :
			time.sleep (0.1)
		self.is_running = True
		T=1 / freq
		TimeOn= round (T * (self.power / 100),4)
		TimeOff = T - TimeOn
		if (self.power == 0): 
				self.is_running = False
		else:
				while self.is_running == True:
					GPIO.output(gpio_num, GPIO.HIGH)
					time.sleep (TimeOn)
					if self.power != 100:
						GPIO.output(self.gpio_num, GPIO.LOW)
					time.sleep (TimeOff)
		GPIO.output(self.gpio_num, GPIO.LOW)
	def stop(self):
		self.is_running = False


class msg:
	def __init__(self,sender,recipient,strType):
		self.sender= sender
		self.recipient= recipient
		self.type = strType
		self.value= None
		self.brocker = MyBrewery.brocker
		self.topic =  MyBrewery.controllerTopic
	def send (self,value):
			
		json_msg = {"sender" : self.sender, "recipient" : self.recipient, "type" : self.type, "value" : value }
		print ("hello")
		json_msg_str= json.dumps (json_msg)
		log ("SEND",json_msg_str)
		client = mqtt.Client()
		client.connect(self.brocker,1883,60)
		client.publish(self.topic, json_msg_str)
		client.disconnect()

def send_msg (sender, recipient, strType, value):
	json_msg = {"sender" : sender, "recipient" : recipient, "type" : strType, "value" : value }
	send_msg (MyBrewery.controllerTopic,json.dumps (json_msg))


def log (strType, strMsg):
	print (strType + "," + strMsg)