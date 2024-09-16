###############################################################
#                                                             #
# ball_valve.py --  ball valve engine display component       #
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


class Ball_Valve(SDR_component_template.Component):

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

        # Init template
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
				fluid_color=kwargs.get('fluid_color', 
							           '#41d94d')
										         )

        self.fill = self.canvas.create_rectangle(
                (width /4.0)    , 
                (height/4.0)    , 
                (width *(3/4.0)), 
                (height*(3/4.0)), 
                fill='#ab1f1f'
                                                )

        self.fillGreen = self.canvas.create_rectangle(
                (width /4.0)    , 
                (height/4.0)    , 
                (width /4.0)    , 
                (height*(3/4.0)), 
                fill='#41d94d'
                                                     )

        self.rect = self.canvas.create_rectangle(
                width /4.0    , 
                height/4.0    ,
                width *(3/4.0), 
                height*(3/4.0), 
                outline='white'
                                                )

        self.percentage = self.canvas.create_text(
                width/2.0, 
                height/2.0, 
                font=("Arial", 10, 'bold'), 
                fill="white", 
                text=" 0%"
                                                 )

        self.per = 0

    def setPercentage(self, p):
        self.per = p
        self.canvas.itemconfig(
                              self.percentage, 
                              text=str(p)+' %'
                              )

        self.canvas.coords(
                          self.fillGreen, 
                          (self.width/4.0), 
                          (self.height/4.0), 
                          (self.width/4.0) + 
                          ((p/100.0)*self.width/2.0), 
                          (self.height*(3/4.0))
                          )

    def getPercentage(self):
        return self.per


###############################################################
# END OF FILE                                                 #
###############################################################
