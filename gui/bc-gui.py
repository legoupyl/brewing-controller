from PIL import Image, ImageTk 
import tkinter as tk 

mlt_temp= 66
bk_temp= 95
hlt_temp= 65
root = tk.Tk()
#root.attributes('-zoomed', True)
img = Image.open("brasserie.bmp")
tkimage = ImageTk.PhotoImage(img)



root.mainloop()