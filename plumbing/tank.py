###############################################################
#                                                             #
# tank.py -- Tank engine display component                    #
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
# Project Imports                                             #
###############################################################
import component_template as SDR_component_template


class Tank:

    def __init__(
                self      , 
                root      ,  # Window to draw on 
                bg_color  ,  # Background color 
                title     ,   
                fluidColor,  # Color of tank fluid 
                width     ,  # Width of drawing canvas 
                height       # Height of drawing canvas
                ):

		# Widget variables
        padding     = 15
        self.width  = width
        self.height = height

        # Booleans indicating which connecting pipes contain fluid
        self.top    = None
        self.right  = None
        self.bottom = None
        self.left   = None

	    # Canvas object to draw on	
        self.canvas = Canvas(
                            root, 
                            width=width, 
                            height=height, 
                            bg=bg_color, 
                            highlightthickness=0
                            )

		# Draw tank and fluid
        self.rect = self.canvas.create_rectangle(
                            width/4.0    , 
                            0            , 
                            width*(3/4.0), 
                            height-1     , 
                            outline='white'
                                                )
        self.fill = self.canvas.create_rectangle(
                            (width/4.0)+1, 
                             50,
                             width*(3/4.0)-1, 
                             height-2, 
                             fill=fluidColor
                                                )
		# Draw tank labels and readouts
        self.pressure = self.canvas.create_text(
                             width/2.0, 
                            (height/2.0)-1.25*padding, 
                             font=("Arial", 11, 'bold'), 
                             fill="white", 
                             text=title
                                               )
        self.pressure = self.canvas.create_text(
                             width/2.0, 
                            (height/2.0), 
                             font=("Arial", 8), 
                             fill="white", 
                             text='psi'
                                               )
        self.percentage = self.canvas.create_text(
                            width /2.0, 
                           (height/2.0)+padding, 
                            font=("Arial", 8), 
                            fill="white", 
                            text='%'
                                                 )
        self.temperature = self.canvas.create_text(
                            width/2.0, 
                           (height/2.0)+2*padding, 
                            font=("Arial", 8), 
                            fill="white", 
                            text='tmp'
                                                  )


    def setTankLevel(self, percent):
        self.canvas.coords(self.fill, (self.width/4.0) + 1, self.height - ((percent/100.0)*self.height-2) - 2, self.width*(3/4.0)-1, self.height-2)
        self.canvas.itemconfig(self.percentage, text=str(percent) + " %")

    def setTankReadout(self, tmp, pressure):
        self.canvas.itemconfig(self.pressure, text=str(pressure) + ' psi')
        self.canvas.itemconfig(self.temperature, text=str(tmp) + ' °C')

    def setNeighbors(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def getWidget(self):
        return self.canvas


###############################################################
# END OF FILE                                                 #
###############################################################
