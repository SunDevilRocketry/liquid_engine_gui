###############################################################
#                                                             #
# valve.py -- contains objects for individual valve control   #
#             buttons                                         #
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
import tkinter as tk


###############################################################
# Global variables                                            #
###############################################################
pad      = 10
sl_width = 500


###############################################################
# Valve state indication light                                #
###############################################################
class Indicator_Light:

    def __init__(
                self, 
                root, 
                bg_color, 
                ):

		#######################################################
		# class attributes                                    #
		#######################################################

		# Canvas dimensions
        self.width  = 60
        self.height = 60

		# Color hex codes
        self.on_color  = '#41d94d'
        self.off_color = '#ed3b3b'


		#######################################################
		# drawing objects                                     #
		#######################################################

		# tk canvas object	
        self.canvas = Canvas(
                            root, 
                            width=self.width, 
                            height=self.height, 
                            bg=bg_color, 
                            highlightthickness=0
                            )

		# indicator circle
        indicator_x0 = 16 # upper left corner coordinates
        indicator_y0 = 16
        indicator_x1 = 44 # lower right corner coordinates
        indicator_y1 = 44
        self.state = self.canvas.create_oval(
                                            indicator_x0, 
                                            indicator_y0, 
                                            indicator_x1, 
                                            indicator_y1, 
                                            fill=self.off_color
                                            )

    def setState(self, state):
        if(state):
            self.canvas.itemconfig(self.state, fill=self.on_color)
        else:
            self.canvas.itemconfig(self.state, fill=self.off_color)

    def getWidget(self):
        return self.canvas


###############################################################
# Solenoid state control buttons                              #
###############################################################
class Buttons:
    def __init__(
                self, 
                root,     # frame to attach button to
                text,     # valve button frame label 
                symbol    # link to engine schematic symbol
                ):

		#######################################################
		# class attributes                                    #
		#######################################################

		# engine schematic symbol link
        self.symbol = symbol

		# valve ON/OFF state
        self.state = 0

		#######################################################
		# objects                                             #
		#######################################################

		# valve button frame
        self.switch = tk.LabelFrame(
                                   root, 
                                   background = 'black',
                                   foreground = 'white',
                                   text = text,
                                   font ='Verdana 12',
                                   relief ='solid',
                                   labelanchor ='n'
                                   )
	
		# indicator light (canvas)
        self.led =  Indicator_Light(
                                   self.switch, 
                                   'black'
                                   )

		# ON/OFF button widgets
        self.off_button = tk.Button(
                                   self.switch, 
                                   text="OFF", 
                                   width=12, 
                                   command=self.actionOff, 
                                   bg='#ed3b3b', 
                                   fg='white', 
                                   activebackground='#d42f2f', 
                                   activeforeground='white'
                                   )

        self.on_button = tk.Button(
                                  self.switch, 
                                  text="ON", 
                                  width=12, 
                                  command=self.actionOn, 
                                  bg='#41d94d', 
                                  fg='white', 
                                  activebackground='#28bd33', 
                                  activeforeground='white'
                                  )

		#######################################################
		# Initial draw                                        #
		#######################################################
        self.off_button.pack(side="right")
        self.led.getWidget().pack(side="right")
        self.on_button.pack(side="right")
        self.switch.pack(side='left', padx=4*pad)

    def actionOff(self):
        self.led.setState(False)
        self.symbol.setState(False)
        print("1 (OFF)")

    def actionOn(self):
        self.led.setState(True)
        self.symbol.setState(True)
        print("1 (ON)")

    def getFrame(self):
        return self.switch


###############################################################
# Ball valve state control buttons                            #
###############################################################
class BV_button:
    def __init__(self, root, text):

		#######################################################
		# class attributes                                    #
		#######################################################

		# valve ON/OFF state
        self.state = 0

		#######################################################
		# objects                                             #
		#######################################################

		# valve button frame
        self.switch = tk.LabelFrame(
                                   root, 
                                   background = 'black',
                                   foreground = 'white',
                                   text=text,
                                   font='Verdana 12',
                                   relief='solid',
                                   labelanchor='n'
                                   )

		# indicator light (canvas)
        self.led  = Indicator_Light(
                                   self.switch,
                                   'black'
                                   )

		# ON/OFF button widgets
        self.on_button  = tk.Button(
                                   self.switch, 
                                   text="ON", 
                                   width=12, 
                                   command=self.actionOn, 
                                   bg='#41d94d', 
                                   fg='white', 
                                   activebackground='#28bd33', 
                                   activeforeground='white'
                                   )

        self.off_button = tk.Button(
                                   self.switch, 
                                   text="OFF", 
                                   width=12, 
                                   command=self.actionOff, 
                                   bg='#ed3b3b', 
                                   fg='white', 
                                   activebackground='#d42f2f', 
                                   activeforeground='white'
                                   )

		#######################################################
		# Initial draw                                        #
		#######################################################
        self.off_button.pack(side="right")
        self.led.getWidget().pack(side="right")
        self.on_button.pack(side="right")
        self.switch.pack(side='left', padx=4*pad)

    def actionOff(self):
        self.led.setState(False)
        print("1 (OFF)")

    def actionOn(self):
        self.led.setState(True)
        print("1 (ON)")

    def getFrame(self):
        return self.switch

        serialNum = int(self.state.get())
        self.lR.config(bg="red")
        print(str(serialNum))

###############################################################
# END OF FILE                                                 #
###############################################################
