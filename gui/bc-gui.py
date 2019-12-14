import threading
from tkinter import *
import time
import sys






# Set variable
MLT_temp = 60.0

BK_temp =98.2
BK_power_setpoint = 85

HLT_temp= 70.1
HLT_temp_setpoint = 69.0

def gui():

    app = Tk()

    FontSize1=100
    FontSize2=80
    y1=150
    y2=400
    #img = Image.open("brasserie.bmp")

    app.geometry("1024x563")
    #app.resizable(width=False, height=False)

    img = PhotoImage(master=app,file = 'brasserie.png')
    canvas = Canvas(app, width=1024, height=563)
    canvas.create_image(512, 282, image=img)
    canvas.grid()


    MLT_temp_txt=canvas.create_text(170, y1, font=('batmfa.ttf', FontSize1), text=MLT_temp , fill='orange')
  

    BK_temp_txt=canvas.create_text(512, y1, font=('batmfa.ttf', FontSize1), text=BK_temp, fill='orange')
    BK_temp_setpoint_txt=canvas.create_text(512, y2, font=('batmfa.ttf', FontSize2), text=BK_power_setpoint, fill='white')

    HLT_temp_txt=canvas.create_text(870, y1, font=('batmfa.ttf', FontSize1), text=HLT_temp, fill='orange')
    HLT_temp_setpoint_txt=canvas.create_text(870, y2, font=('batmfa.ttf', FontSize2), text=HLT_temp_setpoint, fill='white')

    
    app.mainloop ()


def get_MLT_temp():
    global MLT_temp
    while True:
        print (MLT_temp)
        time.sleep(1)
        if  MLT_temp < 70:
            MLT_temp=MLT_temp+0.1
        else:
            MLT_temp = 60.0        
            exit()


MLT_temp_thread = threading.Thread(target=get_MLT_temp)
MLT_temp_thread.daemon=True
MLT_temp_thread.start()

gui_thread = threading.Thread(target=gui)
gui_thread.start()

