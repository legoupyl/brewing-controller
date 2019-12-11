from PIL import Image, ImageTk 
import tkinter as tk 

root = tk.Tk()
root.attributes('-zoomed', True)
img = Image.open("brasserie.bmp")
tkimage = ImageTk.PhotoImage(img)
tk.Label(root, image=tkimage).pack()
root.mainloop()