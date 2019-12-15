import threading
import tkinter as tk
import time
import sys
import smbus 
from gpiozero import Button 
import i2cEncoderLibV2

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


# Set variable
MLT_temp = 60.0

BK_temp = 62.1
BK_power_setpoint = 85

HLT_temp= 70.1



# Init rotary encoders 
encconfig=(i2cEncoderLibV2.INT_DATA | i2cEncoderLibV2.WRAP_ENABLE | i2cEncoderLibV2.DIRE_RIGHT | i2cEncoderLibV2.IPUP_ENABLE | i2cEncoderLibV2.RMOD_X1 | i2cEncoderLibV2.RGB_ENCODER)

HLT_encoder = i2cEncoderLibV2.i2cEncoderLibV2(bus,0x03)
HLT_encoder.begin(encconfig)
HLT_encoder.writeCounter(50)
HLT_encoder.writeMax(90)
HLT_encoder.writeMin(50)
HLT_encoder.writeStep(1)
HLT_encoder.writeInterruptConfig(0xff)

def HLT_encoder_fnc():
    global HLT_temp_setpoint
    HLT_temp_setpoint = 50
    while True:
	if int_pin.is_pressed :
		encoder.updateStatus()
		if HLT_encoder.readStatus(i2cEncoderLibV2.RINC) == True :
			print ('Increment: %d' % (HLT_encoder.readCounter32())) 
		elif HLT_encoder.readStatus(i2cEncoderLibV2.RDEC) == True :
			print ('Decrement:  %d' % (HLT_encoder.readCounter32())) 
		if HLT_encoder.readStatus(i2cEncoderLibV2.RMAX) == True :
			print ('Max!') 
		elif HLT_encoder.readStatus(i2cEncoderLibV2.RMIN) == True :
			print ('Min!') 
        
        HLT_temp_setpoint = encoder.readCounter32()





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

    HLT_temp_label = tk.Label(panel1, text=HLT_temp,bg='black',font=("Helvetica", FontSize1),width=0,height=0,fg='orange')
    HLT_temp_label.place (x=xHLT,y=y1 )
    HLT_temp_setpoint_label=label = tk.Label(panel1, text=HLT_temp_setpoint,bg='black',font=("Helvetica", FontSize2),width=0,height=0,fg='white')
    HLT_temp_setpoint_label.place (x=xHLT+xOffset,y=y2 )


    while True:
        time.sleep (1)
        MLT_temp_label.config (text=round (MLT_temp,1))
        MLT_temp_label.update()
        BK_temp_label.config (text=round (BK_temp,1))
        BK_temp_label.update()
        HLT_temp_label.config (text=round (HLT_temp,1))
        HLT_temp_label.update()




def get_MLT_temp():
    global MLT_temp
    global BK_temp
    global HLT_temp
    while True:
        print (MLT_temp)
        time.sleep(1)
        if  MLT_temp < 70:
            MLT_temp=MLT_temp+0.1
            BK_temp=BK_temp+0.1
            HLT_temp=HLT_temp+0.1


        else:
            MLT_temp = 60.0        
            exit()







MLT_temp_thread = threading.Thread(target=get_MLT_temp)
MLT_temp_thread.daemon=True
MLT_temp_thread.start()


HLT_encoder_thread = threading.Thread(target=HLT_encoder_fnc)
HLT_encoder_thread.daemon=True
HLT_encoder_thread.start()

gui_thread = threading.Thread(target=gui)
gui_thread.start()

