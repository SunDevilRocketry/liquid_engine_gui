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
# Project Imports                                                                    #
######################################################################################
import sequence as SDR_sequence


######################################################################################
# Standard Button Object                                                             #
######################################################################################
class Button:

    # Initialization
    def __init__( 
                 self                  , 
                 root                  , # Widget frame
                 text                  , # Text to display on button
                 size       = (180, 60), # size of button (width, height)
                 corner_r   = 0.2      , # Extent of corner rounding (0.0-1.0)
                 bg_color   = 'black'  , # Color of background
                 f_callback = None     # Button Callback function
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
        corner_radius   = (height/2.0)*corner_r
        corner_diameter = 2*corner_radius

        # Button outline coordinates
        self.button_coords = [
                         [ (corner_radius, 0           ), (width-corner_radius, 0) ],
                         [ (width, height-corner_radius), (width, corner_radius  ) ],
                         [ (width-corner_radius, height), (corner_radius, height ) ],
                         [ (0, height-corner_radius    ), (0, corner_radius      ) ]
                             ]
        self.corner_coords = [
        [ (0,0                               ), (corner_diameter, corner_diameter) ],
        [ (width-corner_diameter, 0          ), (width, corner_diameter          ) ],
        [ (width-corner_diameter,height-corner_diameter), (width, height         ) ],
        [ (0,height-corner_diameter),           (corner_diameter, height         ) ]
                             ]

        # Inner rectangle coordinates
        self.rect_coords = [
            [ (corner_radius, 0           ), (width-corner_radius, height) ],
            [ (0, corner_radius           ), (width, height-corner_radius) ],
                           ]


        ##############################################################################
		# Class Attributes                                                           #
        ##############################################################################

        # Canvas dimensions
        self.width         = width
        self.height        = height
        self.canvas_width  = width  + canvas_pad 
        self.canvas_height = height + canvas_pad 

        # Button corner radius
        self.corner_radius = corner_radius

        # Button callback function
        self.f_callback = f_callback

        # Frame to post to
        self.frame = root

        # Button text
        self.text = text

        # Tk canvas object
        self.canvas = tk.Canvas(
                                root                       ,
                                width  = self.canvas_width ,
                                height = self.canvas_height, 
                                bg     = bg_color          ,
                                highlightthickness = 0
                               )
        
        # Callback functions registrations
        self.canvas.bind( '<Enter>' , self.highlight      )
        self.canvas.bind( '<Leave>' , self.dehighlight    )
        self.canvas.bind( '<Button>', self.action         )
        

        ##############################################################################
		# Initial Draw                                                               #
        ##############################################################################

        # Straight lines
        for line_coords in self.button_coords:
            self.canvas.create_line(
                                    line_coords[0][0], line_coords[0][1], 
                                    line_coords[1][0], line_coords[1][1], 
                                    width = 1, 
                                    fill  = 'white'
                                   )
        
        # Rounded corners
        if ( corner_radius != 0 ):
            for i, corner_coord in enumerate( self.corner_coords ):
                self.canvas.create_arc(
                                       corner_coord[0][0], corner_coord[0][1],
                                       corner_coord[1][0], corner_coord[1][1],
                                       width   = 1        , 
                                       outline = 'white'  ,
                                       start   = 90 - 90*i,
                                       extent  = 90       ,
                                       style   = 'arc'
                                      )

        # Button text
        self.canvas.create_text( width/2, height/2, 
                                 text = text        , 
                                 font = 'Verdana 14', 
                                 fill = 'white' 
                               )

    # Pack the widget into a frame
    def pack( self, side, padx = 60, pady = 30 ):
        self.canvas.pack( side = side, padx = padx, pady = pady )

    # Highlight the button when the mouse hovers over the button
    def highlight( self, event ):

        # Draw Rectangles 
        for rect_coords in self.rect_coords:
            self.canvas.create_rectangle( 
                                         rect_coords[0][0], rect_coords[0][1],
                                         rect_coords[1][0], rect_coords[1][1],
                                         fill = 'white',
                                         outline = 'white'
                                        )

        # Draw Corner ovals
        for corner_coord in self.corner_coords:
            self.canvas.create_oval(
                                    corner_coord[0][0], corner_coord[0][1],
                                    corner_coord[1][0], corner_coord[1][1],
                                    fill = 'white',
                                    outline = 'white'
                                   )
        
        # Draw text 
        self.canvas.create_text( 
                                self.width/2, self.height/2  , 
                                text = self.text   , 
                                font = 'Verdana 14', 
                                fill = 'black' 
                               )

    # Dehighlight the button when the mouse is moved away from the button
    def dehighlight( self, event ):

        # Erase Highlight
        for rect_coords in self.rect_coords:
            self.canvas.create_rectangle( 
                                         rect_coords[0][0], rect_coords[0][1],
                                         rect_coords[1][0], rect_coords[1][1],
                                         fill = 'black'
                                        )
        for corner_coord in self.corner_coords:
            self.canvas.create_oval(
                                    corner_coord[0][0], corner_coord[0][1],
                                    corner_coord[1][0], corner_coord[1][1],
                                    fill = 'black'
                                   )
        # Straight lines
        for line_coords in self.button_coords:
            self.canvas.create_line(
                                    line_coords[0][0], line_coords[0][1], 
                                    line_coords[1][0], line_coords[1][1], 
                                    width = 1, 
                                    fill  = 'white'
                                   )
        
        # Rounded corners
        if ( self.corner_radius != 0 ):
            for i, corner_coord in enumerate( self.corner_coords ):
                self.canvas.create_arc(
                                       corner_coord[0][0], corner_coord[0][1],
                                       corner_coord[1][0], corner_coord[1][1],
                                       width   = 1        , 
                                       outline = 'white'  ,
                                       start   = 90 - 90*i,
                                       extent  = 90       ,
                                       style   = 'arc'
                                      )

        # Button text
        self.canvas.create_text( self.width/2, self.height/2, 
                                 text = self.text           , 
                                 font = 'Verdana 14'        , 
                                 fill = 'white' 
                               )

    # Links callback to button press event 
    def action( self, event ):

        # Call the callback function
        if ( self.f_callback != None ):
            self.f_callback()


######################################################################################
# END OF FILE                                                                        #
######################################################################################