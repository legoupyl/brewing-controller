import tkinter as tk
#from tkinter import StringVar
import time


FontSize1=100
FontSize2=80
#img = Image.open("brasserie.bmp")


root = tk.Tk()
MLT_temp = 50


image1 = tk.PhotoImage(file='brasserie.png')
w = image1.width()
h = image1.height()
root.geometry("%dx%d+0+0" % (w, h))

panel1 = tk.Label(root, image=image1)
panel1.pack(side='top', fill='both', expand='yes')

MLT_temp_label = tk.Label(panel1, text=MLT_temp,bg='black',font=("Helvetica", FontSize1),width=0,height=0,fg='orange')
MLT_temp_label.place (x=75,y=50 )





j = 60

while True:
    if j > 90:
        j=50
    else:
        print (j)
        time.sleep (1)
        j=j+1
        MLT_temp=j
        MLT_temp_label.config (text=j)
        MLT_temp_label.update()

#root.mainloop()