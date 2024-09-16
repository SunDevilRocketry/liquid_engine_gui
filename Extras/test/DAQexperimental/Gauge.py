# !/usr/bin/env python3
import math
from tkinter import *
import tkinter as tk

#UNCOMMENT IF TESTING
import time
import random

class Gauge:

    def __init__(self, root, background, max):
        self.startAngle = -30
        self.endAngle = 210
        self.max = max

        self.c = Canvas(root, width=190, height=190, bg=background, highlightthickness=0)

        #self.xy = [(100.0, 90.0), (100.0, 40.0)]
        #self.line = self.c.create_line(self.xy, width=5, fill='white')
        size = 180
        self.dark = self.c.create_arc(30, 20, size - 10, size - 10, style="arc", width=20, start=self.startAngle, extent=(self.endAngle - self.startAngle)/2.0,
                            outline="#8a1919", tags=('arc1', 'arc2'))
        #1f8749
        self.light = self.c.create_arc(30, 20, size - 10, size - 10, width=20, style="arc", start=90, extent=(self.endAngle - self.startAngle)/2.0,
                             outline="#ff0000", tags=('arc1', 'arc2'))
        #00ff65
        self.readout = self.c.create_text(100, 85, font=("Arial", int(size / 10), 'bold'), fill="white", text='')
        self.label = self.c.create_text(100, 150, font=("Arial", int(size / 14), 'bold'), fill="white", text='')

    def setAngle(self, value): #-30 to 210 value
        theta = self.endAngle - ((value / self.max) * abs(self.endAngle - self.startAngle))
        
        #Gauge bounds set
        if(theta > self.endAngle):
            theta = self.endAngle
        if(theta < self.startAngle):
            theta = self.startAngle

        # NEEDLE ITEMS
        #radius = math.sqrt(pow(self.xy[1][0] - self.xy[0][0], 2) + pow(self.xy[1][1] - self.xy[0][1], 2))
        #y = radius * math.sin(theta * math.pi / 180.0)
        #x = radius * math.cos(theta * math.pi / 180.0)
        #coor = [(100.0, 110.0)]
        #coor.append([self.xy[0][0] + x, self.xy[0][1] - y])
        #self.c.coords(self.line, coor[0][0], coor[0][1], coor[1][0], coor[1][1])
        self.c.itemconfig(self.dark, start=self.startAngle, extent=theta - self.startAngle)
        self.c.itemconfig(self.light, start=theta, extent=self.endAngle - theta)

    def getWidget(self):
        return self.c

    def setText(self, str, label):
        self.c.itemconfig(self.readout, text=str)
        self.c.itemconfig(self.label, text=label)

#TEST CODE
'''win = tk.Tk()
win.title("Guage ELement")
win.geometry("800x200")
win.configure(bg='black')





g = Gauge(win, 'black', -30, 210)
g.getWidget().pack(side='bottom')


while True:

    for i in range(240):
        angle = i - 30
        #random.randint(-10, 190)
        g.setAngle(angle)
        time.sleep(0.01)
        win.update()

    for i in range(240):
        angle = 210 - i
        #random.randint(-10, 190)
        g.setAngle(angle)
        time.sleep(0.01)
        win.update()

win.mainloop()'''