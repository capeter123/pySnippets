from tkinter import *
from tkinter import ttk

lastx, lasty = 0, 0

def xy(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

def addLine(event):
    global lastx, lasty
    canvas.create_line((lastx, lasty, event.x, event.y), fill=color, width=5, tags='currentline')
    lastx, lasty = event.x, event.y


def doneStroke(event):
    canvas.itemconfigure('currentline', width=1)        

color = "black"
def setColor(newcolor):
    print('heeh')
    global color
    color = newcolor

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

canvas = Canvas(root)
canvas.grid(column=0, row=0, sticky=(N, W, E, S))
canvas.bind("<Button-1>", xy)
canvas.bind("<B1-Motion>", addLine)
canvas.bind("<B1-ButtonRelease>", doneStroke)

line1 = canvas.create_line(0, 0, 10, 10, fill='red', tags=('line1'))
canvas.itemconfigure(line1, fill='blue', width=2)
canvas.tag_bind(line1, "<Button-1>", )

rect1 = canvas.create_rectangle((10, 10, 30, 30), fill="red")
canvas.tag_bind(rect1, "<Button-1>", lambda x: setColor("red"))
rect2 = canvas.create_rectangle((10, 35, 30, 55), fill="blue")
canvas.tag_bind(rect2, "<Button-1>", lambda x: setColor("blue"))
rect3 = canvas.create_rectangle((10, 60, 30, 80), fill="black")
canvas.tag_bind(rect3, "<Button-1>", lambda x: setColor("gray"))	

# def setColor(newcolor):
#     global color
#     color = newcolor
#     canvas.dtag('all', 'paletteSelected')
#     canvas.itemconfigure('palette', outline='white')
#     canvas.addtag('paletteSelected', 'withtag', 'palette%s' % color)
#     canvas.itemconfigure('paletteSelected', outline='#999999')

# id = canvas.create_rectangle((10, 10, 30, 30), fill="red", tags=('palette', 'palettered'))
# id = canvas.create_rectangle((10, 35, 30, 55), fill="blue", tags=('palette', 'paletteblue'))
# id = canvas.create_rectangle((10, 60, 30, 80), fill="black", tags=('palette', 'paletteblack', 'paletteSelected'))

# setColor('black')
# canvas.itemconfigure('palette', width=5)

root.mainloop()

# canvas.create_line(10, 10, 200, 50, fill='red', width=3)