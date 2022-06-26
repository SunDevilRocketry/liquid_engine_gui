###############################################################
#                                                             #
# DiagramComponents.py -- Library of engine display           #
#                         components                          #
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
# Engine Component Parent Class                               #
###############################################################
class Component:

    def __init__(
                self, 
                root,        # Window/frame to draw on 
                bg_color,    # Background color
                width,       # Width of drawing canvas 
                height,      # Height of drawing canvas 
                pipe_top,    # Boolean, sets a pipe on top
                             # of component    
                pipe_right,  # Boolean, sets a pipe to the 
                             # right of component
                pipe_buttom, # Boolean, sets a pipe below the
                             # component 
                pipe_left,   # Boolean, sets a pipe to the 
                             # left of component 
                **kwargs
                ):

		#######################################################
		# Class attributes                                    #
		#######################################################

		# Canvas dimensions
        self.width = width
        self.height = height

		# Canvas object
        self.canvas = Canvas(
                            root, 
                            width=width, 
                            height=height, 
                            bg=bg_color, 
                            highlightthickness=0
                            )

        # Pipe input/output port configuration, boolean values
        self.pipe_top    = pipe_top
        self.pipe_right  = pipe_right
        self.pipe_buttom = pipe_buttom
        self.pipe_left   = pipe_left

        # TODO: Not sure what this is yet
        self.top    = None
        self.right  = None
        self.bottom = None
        self.left   = None

        # Fill state boolean variables to tell the GUI how to 
        # draw fluid in the engine pipes
        self.pipe_top_fluid_state    = False
        self.pipe_right_fluid_state  = False
        self.pipe_bottom_fluid_state = False
        self.pipe_left_fluid_state   = False

        # Fluid fill color
        self.fluidColor = kwargs.get('fluid_color', '#41d94d')


		#######################################################
		# Initial component draw                              #
		#######################################################

        # Draw input/output pipes with white lines
        if (pipe_top):
            pipewall_left        = [
                                   (7*width/16.0, height/4.0),
                                   (7*width/16.0, 0)
                                   ]

            self.canvas.create_line(
                                   pipewall_left, 
                                   width=1, 
                                   fill='white'
                                   )

            pipewall_right =       [
                                   (9*width/16.0, height/4.0),
                                   (9*width/16.0, 0)
                                   ]

            self.canvas.create_line(
                                   pipewall_right, 
                                   width=1, 
                                   fill='white'
                                   )
        if (pipe_right):
            pipewall_top =          [
                                    (width*(3/4.0), 7*height/16.0), 
                                    (width        , 7*height/16.0)
                                    ]

            self.canvas.create_line(
                                   pipewall_top, 
                                   width=1, 
                                   fill='white'
                                   )

            pipewall_bottom =      [
                                   (width*(3/4.0), 9*height/16.0), 
                                   (width        , 9*height/16.0)
                                   ]

            self.canvas.create_line(
                                   pipewall_bottom, 
                                   width=1, 
                                   fill='white'
                                   )

        if (pipe_buttom):
            pipewall_left =        [
                                   (7*width/16.0, height*(3/4.0)), 
                                   (7*width/16.0, height)
                                   ]

            self.canvas.create_line(
                                   pipewall_left, 
                                   width=1, 
                                   fill='white'
                                   )

            pipewall_right =       [
                                   (9*width/16.0, height*(3/4.0)), 
                                   (9*width/16.0, height)
                                   ]

            self.canvas.create_line(
                                   pipewall_right, 
                                   width=1, 
                                   fill='white'
                                   )

        if (pipe_left):
            pipewall_top =         [
                                   (width/4.0, 7*height/16.0), 
                                   (0        , 7*height/16.0)
                                   ]

            self.canvas.create_line(
                                   pipewall_top, 
                                   width=1, 
                                   fill='white'
                                   )

            pipewall_bottom =      [
                                   (width/4.0, 9*height/16.0), 
                                   (0        , 9*height/16.0)
                                   ]

            self.canvas.create_line(
                                   pipewall_bottom, 
                                   width=1, 
                                   fill='white'
                                   )

        # Draw inital input/output piping fluid (initially empy)
        self.fluid_top = self.canvas.create_rectangle(
                                                (7*width/16.0)+1, 
                                                 0, 
                                                (9*width/16.0)-1,
                                                ( height/4.0) -1,
                                                fill='black', 
                                                outline=""
                                                     )

        self.fluid_right = self.canvas.create_rectangle(
                                                (3*width /4.0) +1,
                                                (7*height/16.0)+1, 
                                                width,
                                                (9*height/16.0)-1,
                                                fill='black', 
                                                outline=""
                                                       )

        self.fluid_buttom = self.canvas.create_rectangle(
                                               (7*width/16.0)+1, 
                                               (3*height/4.0)+1, 
                                               (9*width/16.0)-1,
                                               height,
                                               fill='black', 
                                               outline=""
                                                        )

        self.fluid_left = self.canvas.create_rectangle(
                                                0, 
                                               (7*height/16.0)+1, 
                                               ( width  / 4.0)-1, 
                                               (9*height/16.0)-1,
                                               fill='black', 
                                               outline=""
                                                      )

	###########################################################
	# Display update drawing functions                        #
	###########################################################

    # Set the fill state of the component input/output pipes and 
    # update the engine display
    def setPipes(self, 
                pipe_top_fluid_state,    # boolean values 
                pipe_right_fluid_state,  # indicating whether  
                pipe_buttom_fluid_state, # there is fluid in the 
                pipe_left_fluid_status   # adjacent pipes
                ):

        # Update class attributes
        self.pipe_top_fluid_state    = pipe_top_fluid_state
        self.pipe_right_fluid_state  = pipe_right_fluid_state
        self.pipe_bottom_fluid_state = pipe_buttom_fluid_state
        self.pipe_left_fluid_state   = pipe_left_fluid_status


        ############# Draw to engine display ##################

        # top pipe
        if (pipe_top_fluid_state):
            self.canvas.itemconfig(
                                  self.fluid_top, 
                                  fill=self.fluidColor
                                  )
        else:
            self.canvas.itemconfig(
                                  self.fluid_top, 
                                  fill='black'
                                  )
        # right pipe
        if (pipe_right_fluid_state):
            self.canvas.itemconfig(
                                  self.fluid_right, 
                                  fill=self.fluidColor
                                  )
        else:
            self.canvas.itemconfig(
                                  self.fluid_right, 
                                  fill='black'
                                  )
        # buttom pipe
        if (pipe_buttom_fluid_state):
            self.canvas.itemconfig(
                                  self.fluid_buttom, 
                                  fill=self.fluidColor
                                  )
        else:
            self.canvas.itemconfig(
                                  self.fluid_buttom, 
                                  fill='black'
                                  )
        # left pipe
        if (pipe_left_fluid_status):
            self.canvas.itemconfig(
                                  self.fluid_left, 
                                  fill=self.fluidColor
                                  )
        else:
            self.canvas.itemconfig(
                                  self.fluid_left, 
                                  fill='black'
                                  )

    # adds fluid to pipes for edge cases
    def setFill(
               self, 
               pipe_top_fluid_state, 
               pipe_right_fluid_state, 
               pipe_buttom_fluid_state, 
               pipe_left_fluid_status
               ):

        # change color only if true
        if (pipe_top_fluid_state):
            self.canvas.itemconfig(
                                  self.fluid_top, 
                                  fill=self.fluidColor
                                  )
        if (pipe_right_fluid_state):
            self.canvas.itemconfig(
                                  self.fluid_right, 
                                  fill=self.fluidColor
                                  )
        if (pipe_buttom_fluid_state):
            self.canvas.itemconfig(
                                  self.fluid_buttom, 
                                  fill=self.fluidColor
                                  )
        if (pipe_left_fluid_status):
            self.canvas.itemconfig(
                                  self.fluid_left, 
                                  fill=self.fluidColor
                                  )

    # TODO: Not sure what this method does
    def setNeighbors(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    # Public access to canvas widget
    def getWidget(self):
        return self.canvas


###############################################################
# END OF FILE                                                 #
###############################################################
