###############################################################
#                                                             #
# gauge.py -- contains gauge object for displaying sensor     #
#             data on GUI                                     #
#                                                             #
# Author: Nitish Chennoju, Colton Acosta                      #
# Date: 6/12/2022                                             #
# Sun Devil Rocketry Avionics                                 #
#                                                             #
###############################################################


###############################################################
# Standard Imports                                            #
###############################################################
from tkinter import *


###############################################################
# Objects                                                     #
###############################################################

# Gauge for displaying sensor data
class gauge:

    def __init__(self, # gauge class 
                 root,       # window to draw gauge on
                 background, # background color
                 max_val     # maximum value to display on 
                             # gauge
                 ):
		
		#######################################################
		# Class attribute initializations                     #
		#######################################################
        self.startAngle = -30      # minimum value guage angle
        self.endAngle   =  210     # maximum value guage angle
        self.max_val    =  max_val # maximum display value
		# Canvas widget for drawing
        self.canvas = Canvas(root, width=190, height=250, bg=background, highlightthickness=0)

        size = 180
        self.dark = self.canvas.create_arc(30, 20, size - 10, size - 10, style="arc", width=20, start=self.startAngle, extent=(self.endAngle - self.startAngle)/2.0,
                            outline="#8a1919", tags=('arc1', 'arc2'))
        #1f8749
        self.light = self.canvas.create_arc(30, 20, size - 10, size - 10, width=20, style="arc", start=90, extent=(self.endAngle - self.startAngle)/2.0,
                             outline="#ff0000", tags=('arc1', 'arc2'))
        #00ff65
        self.readout = self.canvas.create_text(100, 85, font=("Arial", int(size / 10), 'bold'), fill="white", text='')
        self.label = self.canvas.create_text(100, 130, font=("Arial", int(size / 14), 'bold'), fill="white", text='')

    def setAngle(self, value):
        #Gauge bounds set
        theta = self.endAngle - ((value / self.max) * abs(self.endAngle - self.startAngle))

        if(theta > self.endAngle):
            theta = self.endAngle
        if(theta < self.startAngle):
            theta = self.startAngle

        self.canvas.itemconfig(self.dark, start=self.startAngle, extent=theta - self.startAngle)
        self.canvas.itemconfig(self.light, start=theta, extent=self.endAngle - theta)

    def getWidget(self):
        return self.canvas

    def setText(self, str, label):
        self.canvas.itemconfig(self.readout, text=str)
        self.canvas.itemconfig(self.label, text=label)
