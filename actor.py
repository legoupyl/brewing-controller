import sys
import time
from global_settings import *
import paho.mqtt.client as mqtt
from brew_lib import *
import json

pwm_freq=10 #hz
actorName=sys.argv[1]
actor_gpio=sys.argv[2]
pwm_freq=sys.argv[3]
state = 0

def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe(topic)

def on_message(client, userdata, msg):
        mqtt_msg_str=msg.payload.decode()
        print ("Message received : " + mqtt_msg_str)
        try:
            json_msg=json.loads (mqtt_msg_str)
        except Exception as e:
            print(e)
        print ("Actor name :" + actor_name)
        print ("dest:" + json_msg["dest"])
        print ("value:" + str(json_msg["value"]))
        if json_msg["dest"] == actor_name:
            new_state=json_msg["value"]
            state = new_state
            print ("New state received=" + str (new_state))
            json_msg_status = {"sender"=actorName, "senderType": "actor","dest":controller "state":state}
            print ("ACK :" + json.dumps(json_msg_status))
            try: 
                    client.publish (topic,json.dumps (json_msg_status))
            except Exception as e:
                    print(e)  
         
            print ("Send acknowledge")
client = mqtt.Client()

connected = False
while not connected :
        try:
                print ("MQTT Brocker :" + mqtt_brocker)
                print ("Actor topic :" + actor_name )
                client.connect(mqtt_brocker,1883,60)
                client.on_connect = on_connect
                client.on_message = on_message
                client.loop_start()
                connected = True
        except:
                print ("Connection error")
                time.sleep (5)


while 1:
        print ("State :" + str(state))
        time.sleep (round (1 / int(pwm_freq)))