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
HLT_Calib_offset = -0.3
MLT_Calib_offset = -2.5
BK_Calib_offset = -1.3


# Set wiring variable
HLT_pt100_cspin = 18
MLT_pt100_cspin = 19
BK_pt100_cspin = 26


HLT_heater_cspin=24 # or 24
BK_heater_cspin=23

HLT_encoder_cspin=0x10
BK_encoder_cspin=0x03



# Just for variables init
HLT_temp = 0
MLT_temp = 0
BK_temp = 0

HLT_temp_setpoint = 74
MLT_temp_setpoint = 74
BK_power_setpoint = 50


MLT_REGUL_MODE = False


def theEnd():
    print ("Goodbye !")
    GPIO.output(self.BK_heater_cspin, GPIO.LOW)
    GPIO.output(self.HLT_heater_cspin, GPIO.LOW)


class PT100(object):
    # CONFIG PARAMETER & PROPERTIES
    csPin=0
    def __init__(self,csPinValue):
        self.csPin = csPinValue
    print ("csPin=" + str(csPin))
    RefRest = 430
    misoPin = 9
    mosiPin = 10
    clkPin = 11
    config = "0xA2" #ConfigText = Property.Select("Conversion Mode & Wires", options=["[0xB2] - 3 Wires Manual","[0xD2] - 3 Wires Auto","[0xA2] - 2 or 4 Wires Manual","[0xC2] - 2 or 4 Wires Auto"], description="Choose beetween 2, 3 or 4 wire PT100 & the Conversion mode at 60 Hz beetween Manual or Continuous Auto")
 
    def init(self):

        # INIT SENSOR
        self.ConfigReg = self.config
        self.max = max31865.max31865(int(self.csPin),int(self.misoPin), int(self.mosiPin), int(self.clkPin), int(self.RefRest), int(self.ConfigReg,16))

    def read(self):
        n=5
        i=1
        sumTemp=0
        while i<=n:
            sumTemp=sumTemp + self.max.readTemp()
            i=i+1
        return round(sumTemp / n, 2)




# Init rotary encoders 

encconfig=(i2cEncoderLibV2.INT_DATA | i2cEncoderLibV2.WRAP_DISABLE | i2cEncoderLibV2.DIRE_LEFT | i2cEncoderLibV2.IPUP_ENABLE | i2cEncoderLibV2.RMOD_X1 | i2cEncoderLibV2.STD_ENCODER)




def HLT_encoder_fnc():
    global HLT_temp_setpoint
    global MLT_REGUL_MODE
    global MLT_temp_setpoint
    HLT_encoder = i2cEncoderLibV2.i2cEncoderLibV2(bus,HLT_encoder_cspin)
    HLT_encoder.begin(encconfig)
    HLT_encoder.writeCounter(74)
    HLT_encoder.writeMin(0)
    HLT_encoder.writeMax(100)
    HLT_encoder.writeStep(1)
    HLT_encoder.writeDoublePushPeriod (50)
    HLT_encoder.writeInterruptConfig(0xff)
    while True:
        #if HLT_encoder_int_pin.is_pressed :
        HLT_encoder.updateStatus()
        if HLT_encoder.readStatus(i2cEncoderLibV2.RINC) == True :
            print ('Increment: %d' % (HLT_encoder.readCounter32())) 
        elif HLT_encoder.readStatus(i2cEncoderLibV2.RDEC) == True :
            print ('Decrement:  %d' % (HLT_encoder.readCounter32())) 
        if HLT_encoder.readStatus(i2cEncoderLibV2.RMAX) == True :
            print ('Max!') 
        elif HLT_encoder.readStatus(i2cEncoderLibV2.RMIN) == True :
            print ('Min!') 
        if HLT_encoder.readStatus (i2cEncoderLibV2.PUSHP) == True:
            print ("Button Pushed!")
            if MLT_REGUL_MODE:
                MLT_controller.toggle()
            else:
                HLT_controller.toggle()

        if HLT_encoder.readStatus (i2cEncoderLibV2.PUSHD) == True:
            print ("Switching MLT_REGUL_MODE")
            MLT_REGUL_MODE=not MLT_REGUL_MODE
            if not MLT_REGUL_MODE:
                MLT_controller.stop()


        counterValue=round ((HLT_encoder.readCounter32()),1)
        if MLT_REGUL_MODE:
            MLT_temp_setpoint = counterValue
            #HLT_temp_setpoint=MLT_temp_setpoint
        else:
            HLT_temp_setpoint = counterValue
        time.sleep(0.1)



def BK_encoder_fnc():
    global BK_power_setpoint
    BK_encoder = i2cEncoderLibV2.i2cEncoderLibV2(bus,BK_encoder_cspin)
    BK_encoder.begin(encconfig)
    BK_encoder.writeCounter(100)
    BK_encoder.writeMin(0)
    BK_encoder.writeMax(100)
    BK_encoder.writeStep(1)
    BK_encoder.writeDoublePushPeriod(50)
    BK_encoder.writeInterruptConfig(0xff)

    while True:
        #if BK_encoder_int_pin.is_pressed :

        BK_encoder.updateStatus()
        if BK_encoder.readStatus(i2cEncoderLibV2.RINC) == True :
            print ('Increment: %d' % (BK_encoder.readCounter32())) 
        elif BK_encoder.readStatus(i2cEncoderLibV2.RDEC) == True :
            print ('Decrement:  %d' % (BK_encoder.readCounter32())) 
    
        if BK_encoder.readStatus(i2cEncoderLibV2.RMAX) == True :
            print ('Max!') 
        elif BK_encoder.readStatus(i2cEncoderLibV2.RMIN) == True :
            print ('Min!') 
        if BK_encoder.readStatus (i2cEncoderLibV2.PUSHP) == True:
            print ("Button Pushed!")
            BK_controller.toggle()
        if BK_encoder.readStatus (i2cEncoderLibV2.PUSHD) == True:
            print ("Ciao!")
            os.system('sudo shutdown now')
        BK_power_setpoint=BK_encoder.readCounter32()
        time.sleep (0.1)

class BK_controller_class(object):
    def __init__(self):
        print ("Initializing BK controller")
        self.running=False
        self.power =BK_power_setpoint
        self.freq=1
        self.gpio_num=BK_heater_cspin
        
 
    def stop(self):
        self.running = False
        print ("Stopping BK controller")
    def run(self):
        print ("Running BK controller")
        self.running = True
        GPIO.setup(self.gpio_num, GPIO.OUT)
        while (self.running == True):
            self.power=BK_power_setpoint
            T=1/self.freq
            TimeOn=round(T * (self.power / 100),4)
            TimeOff = T - TimeOn

            if not (self.power==0):
                GPIO.output(self.gpio_num, GPIO.HIGH)
                time.sleep (TimeOn)
            if not (self.power == 100):
                GPIO.output(self.gpio_num, GPIO.LOW)
                time.sleep (TimeOff)
        GPIO.output(self.gpio_num, GPIO.LOW)
   
    def start(self):
         print ("Running BK controller")
         if self.running == False:
            
            BK_heater_thread = threading.Thread(target=self.run)
            BK_heater_thread.daemon=True
            BK_heater_thread.start()
    def toggle(self):
        print ("start BK controller toggle" )
        if self.running == False:
            print ("Toggle : Starting BK controller" )
            self.start()
        else:
            print ("Toggle:  Stoping BK controller" )
            self.stop()



class HLT_controller_class(object):
    def __init__(self):
        self.running =False
        self.freq=1
        self.gpio_num=HLT_heater_cspin
        self.power=0
        self.pid=PID(Kp=112.344665712, Ki=0.840663751375, Kd=12.5112685197)
        self.pid.output_limits = (0, 100)
        self.pid.sample_time=5
        self.running=False
        self.pid.proportional_on_measurement = False
    def stop(self):
        print ("Stoping HLT controller" )
        self.running = False
    def run(self):
        self.running = True
        GPIO.setup(self.gpio_num, GPIO.OUT)
        print ("Running  HLT controller" )
        while self.running == True:
            T=1 / self.freq
            TimeOn= round (T * (self.power / 100),4)
            TimeOff = T - TimeOn
            self.pid.setpoint=HLT_temp_setpoint
            self.power = self.pid(HLT_temp)
            if not (self.power==0):
                GPIO.output(self.gpio_num, GPIO.HIGH)
                time.sleep (TimeOn)
            if not (self.power == 100):
                GPIO.output(self.gpio_num, GPIO.LOW)
                time.sleep (TimeOff)
        GPIO.output(self.gpio_num, GPIO.LOW)
    def start(self):
        if self.running == False:
            print ("Starting HLT controller" )
            HLT_heater_thread = threading.Thread(target=self.run)
            HLT_heater_thread.daemon=True
            HLT_heater_thread.start()
 
    def toggle(self):
        if self.running == False:
            print ("Toggle : Starting HLT controller" )
            self.start()
        else:
            self.stop()
            print ("Toggle : Stoping HLT controller" )



#Kp: 111.33691705166814
#Ki: 0.0963955991789334
#Kd: 2030.433776758053
class MLT_controller_class(object):
    #global HLT_temp_setpoint
    def __init__(self):
        self.running =False
        self.power=0
        self.pid=PID(Kp=111.3369, Ki=0.09639, Kd=2030.43377)
        self.pid.output_limits = (0, 1)
        self.pid.sample_time=30
        self.running=False
        self.pid.proportional_on_measurement = False
 
    def stop(self):
        print ("Stoping MLT controller" )
        HLT_controller.stop()
        self.running = False
 
    def run(self):
        global HLT_temp_setpoint
        self.running = True
        print ("Running  MLT controller" )
        while self.running == True:
            time.sleep (30)
            self.pid.setpoint=MLT_temp_setpoint
            self.power = self.pid(MLT_temp)
            HLT_temp_setpoint=MLT_temp_setpoint + self.power
            print ("Auto : HLT temp set point must be" + str(HLT_temp_setpoint))

    def start(self):
        HLT_controller.start()
        if self.running == False:
            print ("Starting MLT controller" )
            MLT_heater_thread = threading.Thread(target=self.run)
            MLT_heater_thread.daemon=True
            MLT_heater_thread.start()
        
 
    def toggle(self):
        if self.running == False:
            print ("Toggle : Starting MLT controller" )
            self.start()
        else:
            self.stop()
            MLT_controller.stop()
            print ("Toggle : Stoping MLT controller" )


def gui():

    root = tk.Tk()
    image1 = tk.PhotoImage(file='Background.png')
    w = image1.width()
    h = image1.height()
    root.geometry("%dx%d+0+0" % (w, h))
    root.attributes('-fullscreen', 1)
    panel1 = tk.Label(root, image=image1)
    panel1.pack(side='top', fill='both', expand='yes')

    MLT_temp_label = tk.Label(panel1, text=MLT_temp,bg='black',font=("Helvetica", FontSize1),width=0,height=0,fg='orange')
    MLT_temp_label.place (x=xMLT,y=y1 )
    MLT_temp_setpoint_label=label = tk.Label(panel1, text=MLT_temp_setpoint,bg='black',font=("Helvetica", FontSize2),width=0,height=0,fg='white')
    MLT_temp_setpoint_label.place (x=xMLT+xOffset2,y=y2 )
    MLT_controller_label = tk.Label(panel1, text="OFF",bg='black',font=("Helvetica", FontSize3),width=0,height=0,fg='white')
    MLT_controller_label.place (x=xMLT+xOffset2,y=y3 )
    MLT_controller_label2 = tk.Label(panel1, text="MLT",bg='black',font=("Helvetica", FontSize3,'bold'),width=0,height=0,fg='#359edb')
    MLT_controller_label2.place (x=xMLT+xOffset2,y=y4 )
    
    
    BK_temp_label = tk.Label(panel1, text=BK_temp,bg='black',font=("Helvetica", FontSize1),width=0,height=0,fg='orange')
    BK_temp_label.place (x=xBK,y=y1 )
    BK_power_setpoint_label=label = tk.Label(panel1, text=str (BK_power_setpoint) + "%",bg='black',font=("Helvetica", FontSize2),width=0,height=0,fg='white')
    BK_power_setpoint_label.place (x=xBK,y=y2 )
    BK_controller_label = tk.Label(panel1, text='OFF',bg='black',font=("Helvetica", FontSize3),width=0,height=0,fg='white')
    BK_controller_label.place (x=xBK+xOffset2,y=y3 )
    BK_controller_label2 = tk.Label(panel1, text='BK',bg='black',font=("Helvetica", FontSize3,'bold'),width=0,height=0,fg='#359edb')
    BK_controller_label2.place (x=xBK+xOffset2,y=y4 )


    HLT_temp_label = tk.Label(panel1, text=HLT_temp,bg='black',font=("Helvetica", FontSize1),width=0,height=0,fg='orange')
    HLT_temp_label.place (x=xHLT,y=y1 )
    HLT_temp_setpoint_label=label = tk.Label(panel1, text=HLT_temp_setpoint,bg='black',font=("Helvetica", FontSize2),width=0,height=0,fg='white')
    HLT_temp_setpoint_label.place (x=xHLT+xOffset2,y=y2 )
    HLT_controller_label = tk.Label(panel1, text="OFF",bg='black',font=("Helvetica", FontSize3),width=0,height=0,fg='white')
    HLT_controller_label.place (x=xHLT+xOffset2,y=y3 )
    HLT_controller_label2 = tk.Label(panel1, text="HLT",bg='black',font=("Helvetica", FontSize3,'bold'),width=0,height=0,fg='#359edb')
    HLT_controller_label2.place (x=xHLT+xOffset2,y=y4 )

    while True:
        time.sleep (0.1)
        MLT_temp_label.config (text=round (MLT_temp,1))
        MLT_temp_label.update()
        BK_temp_label.config (text=round (BK_temp,1))
        BK_temp_label.update()
       
        BK_power_setpoint_label.config (text=str(BK_power_setpoint)+"%")
        BK_power_setpoint_label.update()
        


# MAnaging HLT display
        HLT_temp_label.config (text=round (HLT_temp,1))
        HLT_temp_setpoint_label.config (text=round (HLT_temp_setpoint,1))
        
        if MLT_REGUL_MODE:
            HLT_controller_label.config (text='AUTO')
            HLT_temp_setpoint_label.config (fg='grey')
        else:
            HLT_temp_setpoint_label.config (fg='white')
            if HLT_controller.running:
                HLT_controller_label.config (text='ON')
            else:
                HLT_controller_label.config (text='OFF')
  
        if HLT_controller.running:
            HLT_controller_label.config (fg='red')
        else:
            HLT_controller_label.config (fg='white')

        HLT_temp_label.update()

        HLT_temp_setpoint_label.config (text=round (HLT_temp_setpoint,1))
        HLT_temp_setpoint_label.update()
        HLT_controller_label.update()



        MLT_temp_setpoint_label.config (text=round (MLT_temp_setpoint,1))
        MLT_temp_setpoint_label.update()
        if MLT_controller.running:
            MLT_controller_label.config (text='ON',fg='red')
        else:
            MLT_controller_label.config (text='OFF',fg='white')
        
        MLT_controller_label.update()
        
        if BK_controller.running:
            BK_controller_label.config (text='ON',fg='red')
        else:
            BK_controller_label.config (text='OFF',fg='white')
        BK_controller_label.update()



def get_temp():
    global MLT_temp
    global BK_temp
    global HLT_temp
    MLT_pt100=PT100(csPinValue=MLT_pt100_cspin)
    BK_pt100=PT100(csPinValue=BK_pt100_cspin)
    HLT_pt100=PT100(csPinValue=HLT_pt100_cspin)
 
    print ("init MLT_pt100")
    MLT_pt100.init()
    print ("init BK_pt100")
    BK_pt100.init()
    print ("init HLT_pt100")
    HLT_pt100.init()
    
    while True:
        MLT_temp=MLT_pt100.read() + MLT_Calib_offset
        BK_temp=BK_pt100.read() + BK_Calib_offset
        HLT_temp=HLT_pt100.read() + HLT_Calib_offset
        time.sleep(1)


atexit.register(theEnd)


get_temp_thread = threading.Thread(target=get_temp)
get_temp_thread.daemon=True
get_temp_thread.start()


HLT_controller=HLT_controller_class()
BK_controller=BK_controller_class()
MLT_controller=MLT_controller_class()

time.sleep (1) #waiting controller initialization

BK_encoder_thread = threading.Thread(target=BK_encoder_fnc)
BK_encoder_thread.daemon=True
BK_encoder_thread.start()
time.sleep(1)

HLT_encoder_thread = threading.Thread(target=HLT_encoder_fnc)
HLT_encoder_thread.daemon=True
HLT_encoder_thread.start()
time.sleep(1)
HLT_controller.running=False


gui_thread = threading.Thread(target=gui)
gui_thread.daemon=True
gui_thread.start()
time.sleep(1)
BK_controller.running=False


while  True:
    time.sleep(1)


