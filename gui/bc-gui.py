from PIL import Image, ImageTk 
import tkinter as tk 

root = tk.Tk()
img = Image.open("brasserie.bmp")
tkimage = ImageTk.PhotoImage(img)
tk.Label(root, image=tkimage,text="Hello, world!").pack()
root.mainloop()