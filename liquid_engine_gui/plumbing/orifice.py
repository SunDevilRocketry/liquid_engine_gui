###############################################################
#                                                             #
# orifice.py -- Orifice engine display component              #
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


class Orifice(SDR_component_template.Component):

    def __init__(
                self       , 
                root       , 
                bg_color   , 
                width      , 
                height     , 
                pipe_top   , 
                pipe_right , 
                pipe_buttom, 
                pipe_left  , 
                **kwargs
                ):

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

        self.state = False

        self.rect = self.canvas.create_rectangle(
                width /4.0    , 
                height/4.0    , 
                width *(3/4.0), 
                height*(3/4.0), 
                outline='white'
                                                )

        self.canvas.create_line(
                               (  width/4.0, height/2.0), 
                               (3*width/4.0, height/2.0), 
                               width=1                  , 
                               fill='white'
                               )

        self.beforeP = self.canvas.create_text(
                               width/2.0                , 
                               3*height/8.0             , 
                               font=("Arial", 8, 'bold'), 
                               fill="white"             ,
                               text="B: __ Pa"
                                              )

        self.afterP = self.canvas.create_text(
                               width/2.0                , 
                               5*height/8.0             , 
                               font=("Arial", 8, 'bold'), 
                               fill="white"             ,
                               text="A: __ Pa"
                                             )

        self.name = self.canvas.create_text(
                               width/4.0, 
                               height/8.0, 
                               font=("Arial", 6, 'bold'), 
                               fill="white",
                               text="Orifice"
                                           )

    def setPipes(self, state):
        self.state = state
        if(state):
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
        else:
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

    def getState(self):
        return self.state

    def setValues(self, before, after):
        self.canvas.itemconfig(
                              self.beforeP, 
                              text='B: ' + before + ' Pa'
                              )
        self.canvas.itemconfig(
                              self.afterP, 
                              text='A: ' + after + ' Pa'
                              )


###############################################################
# END OF FILE                                                 #
###############################################################
