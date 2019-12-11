from PIL import Image, ImageTk 
import tkinter as tk 

root = tk.Tk()
Tk.attributes("-fullscreen", True) 
img = Image.open("brasserie.bmp")
tkimage = ImageTk.PhotoImage(img)
tk.Label(root, image=tkimage).pack()
root.mainloop()