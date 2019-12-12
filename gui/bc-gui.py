from tkinter import *
from tkinter import messagebox
app = Tk()


FontSize1=100
FontSize2=80
#img = Image.open("brasserie.bmp")

app.geometry("1024x563")
#app.resizable(width=False, height=False)

img = PhotoImage(file = 'brasserie.png')
canvas = Canvas(app, width=1024, height=563)
canvas.create_image(512, 282, image=img)
canvas.grid()


canvas.create_text(170, 150, font=('batmfa.ttf', FontSize1), text="66.5", fill='red')
canvas.create_text(170, 300, font=('batmfa.ttf', FontSize2), text="70.5", fill='white')

canvas.create_text(512, 150, font=('batmfa.ttf', FontSize1), text="66.5", fill='red')
canvas.create_text(512, 300, font=('batmfa.ttf', FontSize2), text="85%", fill='white')

canvas.create_text(870, 150, font=('batmfa.ttf', FontSize1), text="66.5", fill='red')
canvas.create_text(870, 300, font=('batmfa.ttf', FontSize2), text="77.3", fill='white')


app.mainloop ()

