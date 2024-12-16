###############################################################
#                                                             #
# pressure_sensor.py -- pressure sensor engine display        # 
#                       component                             #
#                                                             #
# Author: Nitish Chennoju, Colton Acosta                      #
# Date: 6/12/2022                                             #
# Sun Devil Rocketry Avionics                                 #
#                                                             #
###############################################################


###############################################################
# Standard Imports                                            #
###############################################################
from liquid_engine_gui.plumbing import component_template as SDR_component_template


class PressureSensor(SDR_component_template.Component):

    def __init__(
                self, 
                root,         # Window to draw on
                bg_color,     # Background color 
                width,        # Width of drawing canvas 
                height,       # Height of drawing canvas 
                pipe_top,     # Pipe connections 
                pipe_right, 
                pipe_buttom, 
                pipe_left, 
                **kwargs      # Fluid color data
                ):

        SDR_component_template.Component.__init__(
               self, 
               root, 
               bg_color, 
               width, 
               height, 
               pipe_top, 
               pipe_right, 
               pipe_buttom, 
               pipe_left, 
               fluid_color=kwargs.get('fluid_color', '#41d94d')
                                                 )

		#######################################################
		# Attribute Initializations                           #
		#######################################################

		# Fluid fill state
        self.state = False

		# Sensor circle coordinates
        pressure_sensor_x0 = width    /4.0  # Upper left corner
        pressure_sensor_y0 = height   /4.0  # coordinates
        pressure_sensor_x1 = width* (3/4.0) # Lower right corner
        pressure_sensor_y1 = height*(3/4.0) # coordinates


		#######################################################
		# Widget Initializations                              #
		#######################################################
		

		# Pressure sensor circle
        self.rect = self.canvas.create_oval(
        		pressure_sensor_x0, 
                pressure_sensor_y0, 
                pressure_sensor_x1, 
                pressure_sensor_y1,
                outline='white', 
                width=1
                                           )

		# Sensor readout
        self.p = self.canvas.create_text(
        		width / 2.0, 
                height / 2.0, 
                font=("Arial", 8, 'bold'), 
                fill="white",
                text="__ Pa"
                                        )

	# Public access to canvas widget
    def getWidget(self):
        return self.canvas

	# Draw fluid in sensor pipes
    def setPipes(self, state):
        self.state = state
        if(state):    # fluid is in connecting pipes
            if (self.pipe_top):
                self.canvas.itemconfig(
                                      self.fluid_top, 
                                      fill=self.fluidColor
                                      )
            if (self.pipe_right):
                self.canvas.itemconfig(
                                      self.fluid_right, 
                                      fill=self.fluidColor
                                      )
            if (self.pipe_buttom):
                self.canvas.itemconfig(
                                      self.fluid_buttom, 
                                      fill=self.fluidColor
                                      )
            if (self.pipe_left):
                self.canvas.itemconfig(
                                      self.fluid_left, 
                                      fill=self.fluidColor
                                      )
        else:	  # no fluid in connecting pipes
            if (self.pipe_top):
                self.canvas.itemconfig(
                                      self.fluid_top, 
                                      fill='black'
                                      )
            if (self.pipe_right):
                self.canvas.itemconfig(
                                      self.fluid_right, 
                                      fill='black'
                                      )
            if (self.pipe_buttom):
                self.canvas.itemconfig(
                                      self.fluid_buttom, 
                                      fill='black'
                                      )
            if (self.pipe_left):
                self.canvas.itemconfig(
                                      self.fluid_left, 
                                      fill='black'
                                      )

	# Set the state indicating if fluid is in the connecting 
    # pipes
    def getState(self):
        return self.state

    # Set the pressure readout
    def setValues(self, pressure):
        self.canvas.itemconfig(self.p, text=pressure)


###############################################################
# END OF FILE                                                 #
###############################################################
