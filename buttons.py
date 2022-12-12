######################################################################################
#                                                                                    #
# buttons.py -- contains custom tk button objects                                    #
#                                                                                    #
# Author: Colton Acosta                                                              #
# Date: 12/10/2022                                                                   #
# Sun Devil Rocketry Avionics                                                        #
#                                                                                    #
######################################################################################


######################################################################################
# Standard Imports                                                                   #
######################################################################################
import tkinter as tk


######################################################################################
# Standard Button Object                                                             #
######################################################################################
class Button:

    # Initialization
    def __init__( 
                 self                , 
                 root                , # Widget frame
                 size     = (180, 60), # size of button (width, height)
                 corner_r = 0.0      , # Extent of corner rounding (0.0-1.0)
                 bg_color = 'black'    # Color of background
                ):

        ##############################################################################
		# Local Draw Variables                                                       #
        ##############################################################################

        # Button dimensions
        width  = size[0]
        height = size[1]

        # Canvas padding to prevent out of bounds drawing
        canvas_pad = 5 

        # Corner Radius percentage
        if   ( corner_r > 1.0 ):
            corner_r = 1.0
        elif ( corner_r < 0.0 ):
            corner_r = 0.0

        # Corner radius
        corner_radius = (height/2.0)*corner_r

        # Button outline coordinates
        button_coords = [
                         [ (corner_radius, 0           ), (width-corner_radius, 0) ],
                         [ (width, height-corner_radius), (width, corner_radius  ) ],
                         [ (width-corner_radius, height), (corner_radius, height ) ],
                         [ (0, height-corner_radius    ), (0, corner_radius      ) ]
                        ]


        ##############################################################################
		# Class Attributes                                                           #
        ##############################################################################

        # Canvas dimensions
        self.width  = width  + canvas_pad 
        self.height = height + canvas_pad 

        # Frame to post to
        self.frame = root

        # Tk canvas object
        self.canvas = tk.Canvas(
                                root                ,
                                width  = self.width ,
                                height = self.height, 
                                bg     = bg_color   ,
                                highlightthickness = 0
                               )
        

        ##############################################################################
		# Initial Draw                                                               #
        ##############################################################################

        for coord in button_coords :
            self.canvas.create_line(
                                    coord[0][0], coord[0][1], 
                                    coord[1][0], coord[1][1], 
                                    width = 1, 
                                    fill  = 'white'
                                   )

    # Pack the widget into a frame
    def pack( self, side ):
        self.canvas.pack( side = side, padx = 60, pady = 30 )


######################################################################################
# END OF FILE                                                                        #
######################################################################################
