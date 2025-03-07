####################################################################################
#                                                                                  #
# valve.py -- contains objects for individual valve control buttons                #
#                                                                                  #
# Author: Nitish Chennoju, Colton Acosta                                           #
# Date: 6/12/2022                                                                  #
# Sun Devil Rocketry Avionics                                                      #
#                                                                                  #
####################################################################################


####################################################################################
# Standard Imports                                                                 #
####################################################################################
from tkinter import *
import tkinter as tk


####################################################################################
# Project Imports                                                                  #
####################################################################################
import buttons as SDR_buttons


####################################################################################
# Global variables                                                                 #
####################################################################################

# Drawing Parameters
pad      = 10
sl_width = 500

# Valve open/close states
VALVE_OPEN   = True
VALVE_CLOSED = False


####################################################################################
# Valve state control buttons                                                      #
####################################################################################
class Buttons:
    def __init__(
                self, 
                root,          # frame to attach button to
                text,          # valve button frame label,
                side,          # Where to place the widget in root 
                symbol=None,   # link to engine schematic symbol
                f_callback  = None
                ):

        ############################################################################
		# class attributes                                                         #
        ############################################################################

		# engine schematic symbol link
        self.symbol = symbol

		# valve OPEN/CLOSE state
        self.state  = VALVE_CLOSED 

        # OPEN/CLOSED colors
        self.closed_color = '#ed3b3b'
        self.open_color   = '#41d94d' 
        self.color        = self.closed_color

        # OPEN/CLOSED texts
        self.closed_text = "CLOSE"
        self.open_text   = "OPEN"
        self.text        = self.closed_text 

        ############################################################################
		# objects                                                                  #
        ############################################################################

		# valve button frame
        self.switch = tk.LabelFrame(
                                   root, 
                                   background  = 'black',
                                   foreground  = 'white',
                                   text        = text,
                                   font        =('Verdana', 12),
                                   relief      ='solid',
                                   labelanchor ='n'
                                   )
	
        # Button Widgets
        if ( f_callback != None ):
            self.button  = SDR_buttons.Button(
                                            self.switch,
                                            text          = self.text , 
                                            size          = (100, 20) ,
                                            corner_r      = 0.2       ,
                                            bg_color      = 'black'   ,
                                            text_color    = self.color,
                                            outline_color = self.color, 
                                            fg_color      = self.color,
                                            f_callback    = f_callback 
                                            )
        else:
            self.button  = SDR_buttons.Button(
                                            self.switch,
                                            text          = self.text , 
                                            size          = (100, 20) ,
                                            corner_r      = 0.2       ,
                                            bg_color      = 'black'   ,
                                            text_color    = self.color,
                                            outline_color = self.color, 
                                            fg_color      = self.color,
                                            f_callback    = self.action 
                                            )


        ############################################################################
		# Initial draw                                                             #
        ############################################################################
        self.button.pack( side = TOP , padx = 5, pady = 5 )
        self.switch.pack( side = side, padx = 20 )


    ################################################################################
    # Update the button color                                                      #
    ################################################################################
    def updateColor( self ):
        if ( self.state == VALVE_CLOSED ):
            self.color = self.closed_color
        else:
            self.color = self.open_color
    ## updateColor ##
    

    ################################################################################
    # Update the button text                                                       #
    ################################################################################
    def updateText( self ):
        if ( self.state == VALVE_CLOSED ):
            self.text = self.closed_text
        else:
            self.text = self.open_text
    ## updateText ##
    

    ################################################################################
    # Configure the button                                                         #
    ################################################################################
    def configButton( self ):
        self.button.text_color    = self.color
        self.button.outline_color = self.color
        self.button.fg_color      = self.color
        self.button.text          = self.text
    ## configButton ##


    ################################################################################
    # Open/Close the valve                                                         #
    ################################################################################
    def action(self):
        if (self.symbol != None):
            self.state = not self.state 
            self.symbol.setState( self.state )
            self.updateText()
            self.updateColor()
            self.configButton()
    ## action ##


    ################################################################################
    # Return the label widget                                                      #
    ################################################################################
    def getFrame(self):
        return self.switch
    ## getFrame ##


####################################################################################
# END OF FILE                                                                      #
####################################################################################