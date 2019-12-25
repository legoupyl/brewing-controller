import threading
import tkinter as tk
import time
import sys
import smbus 
from gpiozero import Button 
import i2cEncoderLibV2
import max31865
from simple_pid import PID


bus=smbus.SMBus(1)


BK_encoder_int_pin= Button(8)
HLT_encoder_int_pin = Button(4)


FontSize1=100
FontSize2=80
y1=50
y2=200
y3= 400

xMLT=35
xBK=380
xHLT= 730

xOffset = 20


# Set wiring variable

MLT_pt100_cspin = 10
BK_pt100_cspin = 11
HLT_pt100_cspin = 12


# Just for variables init
MLT_temp = 0
BK_temp = 0
BK_temp = 0
HLT_temp_setpoint = 74
BK_power_setpoint = 100




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




# Init rotary encoders 
encconfig=(i2cEncoderLibV2.INT_DATA | i2cEncoderLibV2.WRAP_ENABLE | i2cEncoderLibV2.DIRE_LEFT | i2cEncoderLibV2.IPUP_ENABLE | i2cEncoderLibV2.RMOD_X1 | i2cEncoderLibV2.RGB_ENCODER)

HLT_encoder = i2cEncoderLibV2.i2cEncoderLibV2(bus,0x03)
HLT_encoder.begin(encconfig)
HLT_encoder.writeCounter(148)
HLT_encoder.writeMin(100)
HLT_encoder.writeMax(200)
HLT_encoder.writeStep(1)
HLT_encoder.writeInterruptConfig(0xff)

def HLT_encoder_fnc():
    global HLT_temp_setpoint
    while True:
        if HLT_encoder_int_pin.is_pressed :
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
                BK_controller.toggle()
            HLT_temp_setpoint = round ((HLT_encoder.readCounter32() /2),1)

BK_encoder = i2cEncoderLibV2.i2cEncoderLibV2(bus,0x05)
BK_encoder.begin(encconfig)
BK_encoder.writeCounter(100)
BK_encoder.writeMin(0)
BK_encoder.writeMax(100)
BK_encoder.writeStep(1)
BK_encoder.writeInterruptConfig(0xff)


def BK_encoder_fnc():
    global BK_power_setpoint
    while True:
        if BK_encoder_int_pin.is_pressed :
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
            BK_power_setpoint = BK_encoder.readCounter32()

class BK_controller_class(object):
    def __init__(self):
        self.running =False
        self.power =BK_power_setpoint
        freq=1
        gpio_num=21
 
    def stop(self):
        self.running = False
    def start(self):
        self.running = True
        while (running == True):
            power =self.power
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

    def toggle(self):
        if self.running = False:
            self.start()
        else:
            self.true()

class HLT_controller_class(object):
    def __init__(self):
        self.running =False
        freq=1
        gpio_num=22
        power=100
    def stop(self):
        self.running = False
    def start(self):
        running = True
        while running == True:
            T=1 / self.freq
            TimeOn= round (T * (self.power / 100),4)
            TimeOff = T - TimeOn
            if not (self.power==0):
                GPIO.output(self.gpio_num, GPIO.HIGH)
                time.sleep (TimeOn)
            if not (self.power == 100):
                GPIO.output(self.gpio_num, GPIO.LOW)
                time.sleep (TimeOff)
        GPIO.output(self.gpio_num, GPIO.LOW)
    def toggle(self):
        if self.running = False:
            self.start()
        else:
            self.stop()





def gui():

    root = tk.Tk()


    image1 = tk.PhotoImage(file='brasserie.png')
    w = image1.width()
    h = image1.height()
    root.geometry("%dx%d+0+0" % (w, h))

    panel1 = tk.Label(root, image=image1)
    panel1.pack(side='top', fill='both', expand='yes')

    MLT_temp_label = tk.Label(panel1, text=MLT_temp,bg='black',font=("Helvetica", FontSize1),width=0,height=0,fg='orange')
    MLT_temp_label.place (x=xMLT,y=y1 )
  

    BK_temp_label = tk.Label(panel1, text=BK_temp,bg='black',font=("Helvetica", FontSize1),width=0,height=0,fg='orange')
    BK_temp_label.place (x=xBK,y=y1 )
    BK_power_setpoint_label=label = tk.Label(panel1, text=str (BK_power_setpoint) + "%",bg='black',font=("Helvetica", FontSize2),width=0,height=0,fg='white')
    BK_power_setpoint_label.place (x=xBK+xOffset,y=y2 )
    BK_controller_label = tk.Label(panel1, text="Off",bg='black',font=("Helvetica", FontSize1),width=0,height=0,fg='white')
    BK_controller_label.place (x=xBK,y=y3 )


    HLT_temp_label = tk.Label(panel1, text=HLT_temp,bg='black',font=("Helvetica", FontSize1),width=0,height=0,fg='orange')
    HLT_temp_label.place (x=xHLT,y=y1 )
    HLT_temp_setpoint_label=label = tk.Label(panel1, text=HLT_temp_setpoint,bg='black',font=("Helvetica", FontSize2),width=0,height=0,fg='white')
    HLT_temp_setpoint_label.place (x=xHLT+xOffset,y=y2 )
    HLT_controller_label = tk.Label(panel1, text="OFF",bg='black',font=("Helvetica", FontSize1),width=0,height=0,fg='white')
    HLT_controller_label.place (x=xHLT+xOffset,y=y3 )

    while True:
        time.sleep (0.1)
        MLT_temp_label.config (text=round (MLT_temp,1))
        MLT_temp_label.update()
        BK_temp_label.config (text=round (BK_temp,1))
        BK_temp_label.update()
        HLT_temp_label.config (text=round (HLT_temp,1))
        HLT_temp_label.update()

        HLT_temp_setpoint_label.config (text=round (HLT_temp_setpoint,1))
        HLT_temp_setpoint_label.update()
        
        if HLT_controller.running:
            HLT_controller_label.config (text="ON")
        else:
            HLT_controller_label.config (text="OFF")
        HLT_controller_label.update()

        if BK_controller.running:
            BK_controller_label.config (text="ON")
        else:
            BK_controller_label.config (text="OFF")
        BK_controller_label.update()



def get_temp():
    global MLT_temp
    global BK_temp
    global HLT_temp
    MLT_pt100=PT100(csPinValue=MLT_pt100_cspin)
    BK_pt100=PT100(csPinValue=BK_pt100_cspin)
    HLT_pt100=PT100(csPinValue=MLT_pt100_cspin)
    MLT_pt100.init()
    BK_pt100.init()
    HLT_pt100.init()
    while True:
        MLT_temp=MLT_pt100.read()
        BK_temp=BK_pt100.read()
        HLT_temp=HLT_pt100.read()
        time.sleep(1)

get_temp_thread = threading.Thread(target=get_temp)
get_temp_thread.daemon=True
get_temp_thread.start()


HLT_controller=HLT_controller_class()
BK_controller=BK_controller_class()

HLT_encoder_thread = threading.Thread(target=HLT_encoder_fnc)
HLT_encoder_thread.daemon=True
HLT_encoder_thread.start()

BK_encoder_thread = threading.Thread(target=BK_encoder_fnc)
BK_encoder_thread.daemon=True
BK_encoder_thread.start()

gui_thread = threading.Thread(target=gui)
gui_thread.start()



