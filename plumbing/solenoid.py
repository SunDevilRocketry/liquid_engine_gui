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
# Standard Imports                                            #
###############################################################
import DiagramComponents as SDR_DiagramComponents


class Solenoid(SDR_DiagramComponents.Component):
    def __init__(
                self, 
                root, 
                bg_color, 
                num, 
                width, 
                height, 
                pipe_top, 
                pipe_right, 
                pipe_buttom, 
                pipe_left, 
                **kwargs
                ):

        SDR_DiagramComponents.Component.__init__(self, root, bg_color, width, height, pipe_top, pipe_right, pipe_buttom, pipe_left, fluid_color=kwargs.get('fluid_color', '#41d94d'))
        self.inlet = -1
        self.outlet = -1

        self.state = False

        self.fill = self.canvas.create_rectangle((width / 4.0), (height / 4.0), (width * (3 / 4.0)), (height * (3 / 4.0)),
                                            fill='#ab1f1f')
        self.rect = self.canvas.create_rectangle(width / 4.0, height / 4.0, width * (3 / 4.0), height * (3 / 4.0),
                                            outline='white')
        self.canvas.create_text(width / 2.0, height / 2.0, font=("Arial", 10, 'bold'), fill="white", text=str(num))

    def setIn(self, num):
        self.inlet = num

    def setOut(self, num):
        self.outlet = num

    def getState(self):
        return self.state

    def setState(self, open):
        inlet = False
        if (self.inlet == 1):
            if(self.top is not None and self.top.getState()):
                self.canvas.itemconfig(self.fluid_top, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.fluid_top, fill='black')
        if (self.inlet == 2):
            if(self.right is not None and self.right.getState()):
                self.canvas.itemconfig(self.fluid_right, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.fluid_right, fill='black')
        if (self.inlet == 3):
            if (self.bottom is not None and self.bottom.getState()):
                self.canvas.itemconfig(self.fluid_buttom, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.fluid_buttom, fill='black')
        if (self.inlet == 4):
            if (self.left is not None and self.left.getState()):
                self.canvas.itemconfig(self.fluid_left, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.fluid_left, fill='black')

        if(open):
            self.state = True
            self.canvas.itemconfig(self.fill, fill='#41d94d')
            if (self.outlet == 1):
                if(inlet):
                    self.canvas.itemconfig(self.fluid_top, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.fluid_top, fill='black')
            if (self.outlet == 2):
                if (inlet):
                    self.canvas.itemconfig(self.fluid_right, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.fluid_right, fill='black')
            if (self.outlet == 3):
                if (inlet):
                    self.canvas.itemconfig(self.fluid_buttom, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.fluid_buttom, fill='black')
            if (self.outlet == 4):
                if (inlet):
                    self.canvas.itemconfig(self.fluid_left, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.fluid_left, fill='black')
        else:
            self.state = False
            self.canvas.itemconfig(self.fill, fill = '#ab1f1f')
            if (self.outlet == 1):
                self.canvas.itemconfig(self.fluid_top, fill='black')
            if (self.outlet == 2):
                self.canvas.itemconfig(self.fluid_right, fill='black')
            if (self.outlet == 3):
                self.canvas.itemconfig(self.fluid_buttom, fill='black')
            if (self.outlet == 4):
                self.canvas.itemconfig(self.fluid_left, fill='black')
