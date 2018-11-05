import tkinter as tk
import math

class Example:
    def __init__ (self, master):

        self.scale = 1 #Added

        self.master = master
        self.interval = 0
        self.SizeX, self.SizeY = master.winfo_width(), master.winfo_height()
        #Canvas Frame
        self.SystemCanvasFrame = tk.Frame(master, bg='black')
        self.SystemCanvasFrame.grid(row=0, column=0)

        #Canvas
        self.SystemCanvas = tk.Canvas(self.SystemCanvasFrame, width=int(self.SizeX*0.75)-20, height=self.SizeY-20, bg="black")
        self.SystemCanvas.focus_set()
        self.xsb = tk.Scrollbar(self.SystemCanvasFrame, orient="horizontal", command=self.SystemCanvas.xview)
        self.ysb = tk.Scrollbar(self.SystemCanvasFrame, orient="vertical", command=self.SystemCanvas.yview)
        self.SystemCanvas.configure(scrollregion=(-500,-500,500,500))
        self.SystemCanvas.configure(yscrollcommand=self.ysb.set, xscrollcommand=self.xsb.set)
        #add the canvas with scroll bar in grid format
        self.xsb.grid(row=1, column=0, sticky="ew")
        self.ysb.grid(row=0, column=1, sticky="ns")
        self.SystemCanvas.grid(row=0, column=0, sticky="nsew")

        # This is what enables using the mouse to slide the window:
        self.SystemCanvas.bind("<ButtonPress-1>", self.move_start)
        self.SystemCanvas.bind("<B1-Motion>", self.move_move)
        #windows scroll
        self.SystemCanvas.bind("<MouseWheel>",self.zoomer)        
        #resize the main window
        self.master.bind('<Configure>', self.UpdateCanvasSize)

        #Create Objects
        self.Size = 5 #object Size
        x0 = 0
        y0 = 0
        x1 = self.Size
        y1 = self.Size
        self.SystemCanvas.create_oval(x0,y0,x1,y1, fill='green',   outline='green', width=3, tags='Green')
        self.SystemCanvas.create_oval(x0,y0,x1,y1, fill='red', outline='red', width=3, tags='Red')
        self.SystemCanvas.create_oval(x0,y0,x1,y1, fill='yellow', outline='yellow', width=1, tags='Yellow')

        self.Display()


    #**Added Method
    def update_coord(self, coord):
        """Calculate the scaled cordinate for a given cordinate based on the zoomer scale factor"""
        new_coord = [coord_i * self.scale for coord_i in coord]
        return new_coord


    def Display(self):
        self.interval += 0.5 #speed parameter
        GreenPos = self.UpdatePosition(0.1*self.interval, (0,0), 50)
        RedPos = self.UpdatePosition(0.02*self.interval+180, (0,0), 200)
        YellowPos = self.UpdatePosition(0.3*self.interval, RedPos, 10)

        self.MoveObject('Green', GreenPos)
        self.MoveObject('Red', RedPos)
        self.MoveObject('Yellow', YellowPos)


        self.master.after(1, self.Display) #Disable to zoom

    def MoveObject (self, Obj, pos): #only move object that are in the field of view
        """Move Obj to the given position (tuple - xy)"""
        ID = self.SystemCanvas.find_withtag(Obj)      
        #Convert the Center of the object to the coo need for tk
        x0 = pos[0] - self.Size/2.0 #radius of the circle
        y0 = pos[1] - self.Size/2.0
        x1 = pos[0] + self.Size/2.0
        y1 = pos[1] + self.Size/2.0
        c_0 = self.update_coord([x0, y0]) #Added
        c_1 = self.update_coord([x1, y1]) #Added
        self.SystemCanvas.coords(ID, c_0[0], c_0[1], c_1[0], c_1[1]) #Added/Edited 

    def UpdatePosition(self, angle, center, distance):
        """Calculate next object position around the Center at the Distance and speed determine by Angle (in Radian) - Center of the object"""
        h = center[0]
        k = center[1]
        radius = distance
        Rad = angle
        x = h+radius*math.cos(Rad)
        y = k+radius*math.sin(Rad)
        return self.update_coord([x, y]) #Added/Edited

    def UpdateCanvasSize(self, event):
        """Permit to resize the canvas to the window"""
        self.SizeX, self.SizeY = self.master.winfo_width(), self.master.winfo_height()
        self.SystemCanvas.config(width=int(self.SizeX*0.75)-20, height=self.SizeY-20)

    def move_start(self, event):
        """Detect the beginning of the move"""
        self.SystemCanvas.scan_mark(event.x, event.y)
        self.SystemCanvas.focus_set() #security, set the focus on the Canvas

    def move_move(self, event):
        """Detect the move of the mouse"""
        self.SystemCanvas.scan_dragto(event.x, event.y, gain=1)

    def zoomer(self,event):
        """Detect the zoom action by the mouse. Zoom on the mouse focus"""
        true_x = self.SystemCanvas.canvasx(event.x)
        true_y = self.SystemCanvas.canvasy(event.y)
        if (event.delta > 0):
            self.SystemCanvas.scale("all", true_x, true_y, 1.2, 1.2)
            self.scale *= 1.2 #**Added
        elif (event.delta < 0):
            self.SystemCanvas.scale("all", true_x, true_y, 0.8, 0.8)
            self.scale *= 0.8 #**Added
        #self.SystemCanvas.configure(scrollregion =  self.SystemCanvas.bbox("all")) #**Removed (This disables scrollbar after zoom)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1125x750')
    app = Example(root)
    root.mainloop()