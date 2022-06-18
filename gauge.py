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

	###########################################################
	# Class attribute initializations                         #
	###########################################################
    def __init__(self,          # gauge class 
                 root,          # window to draw gauge on
                 background,    # background color
                 max_sensor_val # maximum value to display on 
                                # gauge
                 ):
		
		# simple variables
        self.startAngle     = -30             # minimum value 
                                              # guage angle
        self.endAngle       =  210            # maximum value 
                                              # guage angle
        self.max_sensor_val =  max_sensor_val # maximum display 
                                              # value
        size                =  180            # size of gauge

		# Canvas widget for drawing
        self.canvas = Canvas(root,          # parent window 
                             width=190,     # canvas dimensions
                             height=250, 
                             bg=background, # background color 
                             highlightthickness=0 
                            )

		# Base gauge arc -- always draws start angle to end angle
        self.gauge_arc = self.canvas.create_arc(
						30, 20,                 # upper left corner
                                                # coordinates 
						size - 10, size - 10,   # lower right corner
                                                # coordinates 
						style="arc", width=20,  # arc width 
						start=self.startAngle,  # minimum drawing 
                                                # angle 
						# drawing angle
						extent=(self.endAngle - self.startAngle)/2.0,
                        outline="#8a1919",      # dark red hex code
                        tags=('arc1', 'arc2')   # arc tags
                                              )
		
		# Fill gauge arc -- draws start angle to display angle
        self.gauge_fill_arc = self.canvas.create_arc(
						30, 20,                 # upper left corner
                                                # coordinates 
						size - 10, size - 10,   # lower right corner
												# coordinates 
						width=20, style="arc",  # arc width 
						start=90,               # minimum drawing angle 
						# drawing angle 
						extent=(self.endAngle - self.startAngle)/2.0,
                        outline="#ff0000",      # light red hex code
                        tags=('arc1', 'arc2')   # arc tags
                                                    )

        # Gauge text for sensor value
        self.readout = self.canvas.create_text(
                        100, 85,               # x-y coordinates
                        font=("Arial",         # font properties
                               int(size / 10), 
                               'bold'), 
                        fill="white",          # text color
                        text=''                # text contents
                                             )

        # Gauge text for sensor name
        self.label = self.canvas.create_text(
						100, 150,             # x-y coordinates
						font=("Arial",        # font properties
                              int(size / 15), 
							  'bold'), 
                        fill="white",         # text color
                        text=''               # text contents
                                            )

	###########################################################
	# API methods                                             #
	###########################################################

	# Set the gauge display angle from sensor values 
    def setAngle(self,        # gauge class 
                 sensor_value # sensor value
                ):

        # Set gauge diplay angle
        gauge_angular_width = abs(self.endAngle - self.startAngle)
        gauge_percent_fill = value/self.max_sensor_val  
        gauge_angle = self.endAngle - (gauge_percent_fill*gauge_angular_width)

		# Saturate gauge fill if sensor value goes out of bounds
        if( gauge_angle > self.endAngle):
            gauge_angle = self.endAngle
			# TODO: log this failure condition
        if( gauge_angle < self.startAngle):
            gauge_angle = self.startAngle
			# TODO: log this failure condition

		# Draw gauge using sensor value
        self.canvas.itemconfig(
				self.gauge_arc,                      # arc object 
                start=self.startAngle,               # start angle 
                extent=gauge_angle - self.startAngle # angular width 
                              )
        self.canvas.itemconfig(
				self.gauge_fill_arc,                # arc object 
				start=gauge_angle,                  # start angle
                extent=self.endAngle - gauge_angle  # angular width
                              ) 

	# Allow public access to canvas object
    def getWidget(self):
        return self.canvas

	# Set the gauge text
    def setText(self, 
                sensor_val,  # sensor display value
                sensor_label # sensor label
               ):
        self.canvas.itemconfig(self.readout, text=sensor_val)
        self.canvas.itemconfig(self.label, text=sensor_label)

###############################################################
# END OF FILE                                                 #
###############################################################
