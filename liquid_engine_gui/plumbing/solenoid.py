###############################################################
#                                                             #
# solenoid.py -- Solenoid engine display component            #
#                                                             #
# Author: Nitish Chennoju, Colton Acosta                      #
# Date: 6/12/2022                                             #
# Sun Devil Rocketry Avionics                                 #
#                                                             #
###############################################################


###############################################################
# Project Imports                                             #
###############################################################
from liquid_engine_gui.plumbing import component_template as SDR_component_template


class Solenoid(SDR_component_template.Component):
    def __init__(
                self       , 
                root       ,    # Window to draw on 
                bg_color   ,    # Background color 
                num        ,         
                width      ,    # Width of draw canvas 
                height     ,    # Height of draw canvas 
                pipe_top   ,    # Connecting pipes fill status 
                pipe_right , 
                pipe_buttom, 
                pipe_left  , 
                **kwargs        # fluid color
                ):

		# Initial component initializations
        SDR_component_template.Component.__init__(
                self       , 
                root       , 
                bg_color   , 
                width      , 
                height     , 
                pipe_top   , 
                pipe_right , 
                pipe_buttom, 
                pipe_left  , 
                fluid_color=kwargs.get('fluid_color', '#41d94d')
                                                  )

	    # Variables indicating which connecting pipes are the 
        # input and output terminals	

		# Initialize to an unused value
        self.inlet =  -1
        self.outlet = -1

		# Constants used to indicate which connecting pipes are input
        # and output
        self.inlet_pipe_top     = 1
        self.inlet_pipe_right   = 2
        self.inlet_pipe_bottom  = 3
        self.inlet_pipe_left    = 4

        self.outlet_pipe_top    = 1
        self.outlet_pipe_right  = 2
        self.outlet_pipe_bottom = 3
        self.outlet_pipe_left   = 4
		
		# Boolean indicating if the solenoid output contains fluid
        self.state = False

		# Draw initial fluid in connecting pipes
        self.fill = self.canvas.create_rectangle(
               (width /4.0)    , 
               (height/4.0)    , 
               (width *(3/4.0)), 
               (height*(3/4.0)),
               fill='#ab1f1f'
                                                )

		# Draw the solenoid outline
        self.rect = self.canvas.create_rectangle(
               width /4.0    , 
               height/4.0    , 
               width *(3/4.0), 
               height*(3/4.0),
               outline='white'
                                                )

		# Write the solenoid number
        self.canvas.create_text(
               width /2.0  , 
               height/2.0  , 
               font=("Arial", 10, 'bold'), 
               fill="white", 
               text=str(num)
                               )

    def setIn(self, num):
        self.inlet = num

    def setOut(self, num):
        self.outlet = num

    def getState(self):
        return self.state

    # Set the solenoid to open or closed
    def setState(
                self, 
                open_solenoid  # Boolean indicating if the solenoid is open
                ):

        inlet = False
		
		# Draw the inlet fluid
        if (self.inlet == self.inlet_pipe_top):
            if(self.top is not None and self.top.getState()):
                self.canvas.itemconfig(self.fluid_top, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.fluid_top, fill='black')
        if (self.inlet == self.inlet_pipe_right):
            if(self.right is not None and self.right.getState()):
                self.canvas.itemconfig(self.fluid_right, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.fluid_right, fill='black')
        if (self.inlet == self.inlet_pipe_bottom):
            if (self.bottom is not None and self.bottom.getState()):
                self.canvas.itemconfig(self.fluid_buttom, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.fluid_buttom, fill='black')
        if (self.inlet == self.inlet_pipe_left):
            if (self.left is not None and self.left.getState()):
                self.canvas.itemconfig(self.fluid_left, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.fluid_left, fill='black')

		# Draw the output fluid 
        if(open_solenoid):
            self.state = True
            self.canvas.itemconfig(self.fill, fill='#41d94d')
            if (self.outlet == self.outlet_pipe_top):
                if(inlet):
                    self.canvas.itemconfig(self.fluid_top, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.fluid_top, fill='black')
            if (self.outlet == self.outlet_pipe_right):
                if (inlet):
                    self.canvas.itemconfig(self.fluid_right, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.fluid_right, fill='black')
            if (self.outlet == self.outlet_pipe_bottom):
                if (inlet):
                    self.canvas.itemconfig(self.fluid_buttom, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.fluid_buttom, fill='black')
            if (self.outlet == self.outlet_pipe_left):
                if (inlet):
                    self.canvas.itemconfig(self.fluid_left, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.fluid_left, fill='black')

        else: # Valve is closed, draw the output pipe black
            self.state = False
            self.canvas.itemconfig(self.fill, fill = '#ab1f1f')
            if (self.outlet == self.outlet_pipe_top):
                self.canvas.itemconfig(self.fluid_top, fill='black')
            if (self.outlet == self.outlet_pipe_right):
                self.canvas.itemconfig(self.fluid_right, fill='black')
            if (self.outlet == self.outlet_pipe_bottom):
                self.canvas.itemconfig(self.fluid_buttom, fill='black')
            if (self.outlet == self.outlet_pipe_left):
                self.canvas.itemconfig(self.fluid_left, fill='black')


###############################################################
# END OF FILE                                                 #
###############################################################
