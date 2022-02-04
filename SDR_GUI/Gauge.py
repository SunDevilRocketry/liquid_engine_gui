# !/usr/bin/env python3
from tkinter import *

#UNCOMMENT IF TESTING
'''import tkinter as tk
import time
import math
import random'''

class Gauge:

    def __init__(self, root, background, max):
        self.startAngle = -30
        self.endAngle = 210
        self.max = max
        self.c = Canvas(root, width=190, height=250, bg=background, highlightthickness=0)

        size = 180
        self.dark = self.c.create_arc(30, 20, size - 10, size - 10, style="arc", width=20, start=self.startAngle, extent=(self.endAngle - self.startAngle)/2.0,
                            outline="#8a1919", tags=('arc1', 'arc2'))
        #1f8749
        self.light = self.c.create_arc(30, 20, size - 10, size - 10, width=20, style="arc", start=90, extent=(self.endAngle - self.startAngle)/2.0,
                             outline="#ff0000", tags=('arc1', 'arc2'))
        #00ff65
        self.readout = self.c.create_text(100, 85, font=("Arial", int(size / 10), 'bold'), fill="white", text='')
        self.label = self.c.create_text(100, 130, font=("Arial", int(size / 14), 'bold'), fill="white", text='')

    def setAngle(self, value):
        #Gauge bounds set
        theta = self.endAngle - ((value / self.max) * abs(self.endAngle - self.startAngle))

        if(theta > self.endAngle):
            theta = self.endAngle
        if(theta < self.startAngle):
            theta = self.startAngle

        self.c.itemconfig(self.dark, start=self.startAngle, extent=theta - self.startAngle)
        self.c.itemconfig(self.light, start=theta, extent=self.endAngle - theta)

    def getWidget(self):
        return self.c

    def setText(self, str, label):
        self.c.itemconfig(self.readout, text=str)
        self.c.itemconfig(self.label, text=label)




#GAUGE TEST CODE
'''win = tk.Tk()
win.title("Gauge ELement")
win.geometry("800x200")
win.configure(bg='black')

g = Gauge(win, 'black', 5)
g.getWidget().pack(side='bottom')
while True:

    for i in range(6):
        g.setAngle(i)
        time.sleep(0.1)
        win.update()

    for i in range(6):
        g.setAngle(5-i)
        time.sleep(0.1)
        win.update()

win.mainloop()'''
