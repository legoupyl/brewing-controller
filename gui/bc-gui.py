import threading

import tkinter as tk
import time
import sys



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
HLT_temp_setpoint = 69.0

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

gui_thread = threading.Thread(target=gui)
gui_thread.start()

