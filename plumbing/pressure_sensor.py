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
import component_template as SDR_component_template


class PressureSensor(SDR_component_template.Component):

    def __init__(self, root, bg_color, width, height, pipe_top, pipe_right, pipe_buttom, pipe_left, **kwargs):

        SDR_component_template.Component.__init__(self, root, bg_color, width, height, pipe_top, pipe_right, pipe_buttom, pipe_left, fluid_color=kwargs.get('fluid_color', '#41d94d'))

        self.state = False

        self.rect = self.canvas.create_oval(width / 4.0, height / 4.0, width * (3 / 4.0), height * (3 / 4.0),
                                            outline='white', width=1)
        self.p = self.canvas.create_text(width / 2.0, height / 2.0, font=("Arial", 8, 'bold'), fill="white",
                                             text="__ Pa")
        self.name = self.canvas.create_text(width/4.0, height/8.0, font=("Arial", 6, 'bold'), fill="white",
                                         text="Pressure\nSensor")

    def getWidget(self):
        return self.canvas

    def setPipes(self, state):
        self.state = state
        if(state):
            if (self.pipe_top):
                self.canvas.itemconfig(self.fluid_top, fill=self.fluidColor)
            if (self.pipe_right):
                self.canvas.itemconfig(self.fluid_right, fill=self.fluidColor)
            if (self.pipe_buttom):
                self.canvas.itemconfig(self.fluid_buttom, fill=self.fluidColor)
            if (self.pipe_left):
                self.canvas.itemconfig(self.fluid_left, fill=self.fluidColor)
        else:
            if (self.pipe_top):
                self.canvas.itemconfig(self.fluid_top, fill='black')
            if (self.pipe_right):
                self.canvas.itemconfig(self.fluid_right, fill='black')
            if (self.pipe_buttom):
                self.canvas.itemconfig(self.fluid_buttom, fill='black')
            if (self.pipe_left):
                self.canvas.itemconfig(self.fluid_left, fill='black')

    def getState(self):
        return self.state

    def setValues(self, pressure):
        self.canvas.itemconfig(self.p, text=pressure)


###############################################################
# END OF FILE                                                 #
###############################################################
