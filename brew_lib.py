import sys
import threading
import time
import json
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from simple_pid import PID

class brewery:
	def __init__(self):
		self.name = "Goupyl's brewery"
		self.brocker ="brocker.legoupyl.com"
		self.controllerTopic = "controller"
		self.HLT = "HLT"
		self.MLT = "MLT"
		self.BT = "BT"

MyBrewery =  brewery ()

def log (strType, strMsg):
	print (str(strType) + "," + str(strMsg))

class listner ():
	def on_connect(self,client, userdata, flags, rc):
		log ("mqqt", "Connected with result code " + str(rc))
		client.subscribe("controller")

	def on_message(self,client, userdata, msg):
			mqtt_msg_str=msg.payload.decode()
			log ("MSG", "Received :" + mqtt_msg_str)
			try:
				json_msg=json.loads (mqtt_msg_str)
				log ("MSG", "Loaded JSON MSG" + mqtt_msg_str )
			
				self.child_on_message(json_msg)
			except Exception as e: 
				print(e)
				pass

	def __init__(self):
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
		self.value= 50
		inc= 0.5
		while self.is_running:
			self.msg.send (self.value)
			self.value= self.value + inc
			if self.value > 100 :
				inc=-0.5
			if self.value < 50 :
				inc=0.5				
			time.sleep (1)
	def stop(self):
		self.is_running = False


class controller (PID,listner):
	def __init__(self, name, type, sensor, actor):
		self.type = "tempController"
		self.name = name
		self.auto = True
		self.state = ""
		self.sensor = sensor
		self.sensorValue= -273
		self.actor ="hlt_heater"
		self.actorValue= 0
		self.contollerSate = "on"
		self.previousControllerSate = self.contollerSate
		self.consoleMsg =msg(self.name,"controller","controllerState")
		self.actorMsg=msg("controller",self.actor,"command")
		PID.__init__ (self,Kp=112.344665712, Ki=0.840663751375, Kd=12.5112685197)
		self.setpoint = 66
		self.output_limits = (0, 100)
		listner.__init__(self)

	
	def child_on_message (self,json_msg):
		if  json_msg ["sender"] == self.sensor:
			self.sensorValue=json_msg ["value"]
			log ("RcvSensorValue", self.sensorValue)
			if self.contollerSate == "on":
				newActorValue = PID.__call__ (self,self.sensorValue)
				log ("PID", "CurrentTemp :" + str(self.sensorValue) + " setpoint : " + str(self.setpoint) + " New actor value :" + str (newActorValue))
				self.actorMsg.send (newActorValue)
		if  json_msg ["sender"] == self.actor:
			self.actorValue= json_msg ["value"]
			log ("RcvActorValue", self.actorValue)
		if  json_msg ["recipient"] == self.name and  json_msg ["sender"] == "console":
			if  json_msg ["type"] == "setpoint":
				self.setpoint = json_msg ["value"]
				log ("RcvActorConsigne", self.actorValue)
			if  json_msg ["type"] == "contollerSate":
				self.contollerSate = json_msg ["value"]
				if self.contollerSate == 0:
					self.actorMsg.send (0) # turn off actor after disabling  controller
				log ("RcvControllerState", self.contollerSate)	
				self.consoleMsg.send (contollerSate)
				log ("SendCurrentControllerState", self.contollerSate)		
	def start ():
		self.run()
	def run ():
		while 1:
			time.sleep (10)




class actor (listner) :
	def __init__(self, name,gpio_num,freq):
		self.name = name
		self.gpio_num=gpio_num
		self.freq=freq
		self.gpio = gpio_pwm (self.gpio_num, self.freq)
		self.contollerMsg = msg (name,"controller","actorState")
		listner.__init__(self)
		
	def child_on_message (self,json_msg):
		if  (json_msg ["recipient"] == self.name and json_msg ["type"] == "command"):
			self.power=json_msg ["value"]
			log ("RcvActorValue", self.actorValue)
			self.msg.send (power)


class gpio_pwm (actor):
	def __init__(self,gpio_num,freq):
		self.gpio_num = gpio_num 
		self.freq = freq
		self.power = 0
		self._is_running=False
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.gpio_num, GPIO.OUT)
		self.start()

	def start (self):
		self.thread = threading.Thread(target=self.run, args=())
		self.thread.daemon = True
		self.is_running = True
		self.thread.start()  

	def run (self):
		self.is_running = True
		while self.is_running :
			T=1 / self.freq
			TimeOn= round (T * (self.power / 100),4)
			TimeOff = T - TimeOn
			if not (self.power==0):
				GPIO.output(self.gpio_num, GPIO.HIGH)
				time.sleep (TimeOn)
			if not (self.power == 100):
				GPIO.output(self.gpio_num, GPIO.LOW)
				time.sleep (TimeOff)
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


