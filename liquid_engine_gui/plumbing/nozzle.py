###############################################################
#                                                             #
# nozzle.py -- Combustion chamber engine display component    #
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
from liquid_engine_gui.plumbing import component_template as SDR_component_template


class Nozzle:

    def __init__(
                self, 
                root, 
                bg_color, 
                width, 
                height
                ):

        padding = 25

        self.top    = None
        self.right  = None
        self.bottom = None
        self.left   = None

        self.canvas = Canvas(
                            root, 
                            width=width, 
                            height=height, 
                            bg=bg_color, 
                            highlightthickness=0
                            )

        self.width = width
        self.height = height

        self.plot = []
        self.plot.append((1, 1))
        self.plot.append((width-1, 1))
        self.plot.append((  width-1, height*0.1))
        self.plot.append((0.9*width, height*0.1))
        self.plot.append((0.9*width, height*0.7))
        self.plot.append((0.6*width, height*0.9))
        self.plot.append((0.7*width, height-1  ))
        self.plot.append((0.3*width, height-1  ))
        self.plot.append((0.4*width, height*0.9))
        self.plot.append((0.1*width, height*0.7))
        self.plot.append((0.1*width, height*0.1))
        self.plot.append((1, height*0.1))

        self.base = self.canvas.create_polygon(
                            self.plot, 
                            outline='white'
                                              )

        self.thrust = self.canvas.create_text(
                            width/2.0           , 
                            (height/2.0)-padding, 
                            font=("Arial", 10)  , 
                            fill="white"        , 
                            text='thrust'
                                             )

        self.pressure = self.canvas.create_text(
                            width/2.0         , 
                            height/2.0        , 
                            font=("Arial", 10), 
                            fill="white"      , 
                            text='pressure'
                                               )


    def setNeighbors(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def getWidget(self):
        return self.canvas

    def setNozzleReadout(self, thrust, pressure):
        self.canvas.itemconfig(
                              self.thrust, 
                              text='LC: ' + 
                              str(thrust) + 
                              ' N'
                              )

        self.canvas.itemconfig(
                              self.pressure, 
                              text='PT: '   + 
                              str(pressure) + 
                              ' psi'
                              )


###############################################################
# END OF FILE                                                 #
###############################################################
