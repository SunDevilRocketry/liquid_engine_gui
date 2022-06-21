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
                root,       # Window/frame to draw on 
                bg_color,   # Background color
                width,      # Width of drawing canvas 
                height,     # Hieght of drawing canvas 
                pipe_top,   # Boolean, sets a pipe on top
                            # of component    
                pipe_right, # Boolean, sets a pipe to the 
                            # right of component
                line_3, 
                line_4, 
                **kwargs
                ):

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

        self.pipe_top = pipe_top
        self.pipe_right = pipe_right
        self.line_3 = line_3
        self.line_4 = line_4

        self.top = None
        self.right = None
        self.bottom = None
        self.left = None
        self.fill1 = False
        self.fill2 = False
        self.fill3 = False
        self.fill4 = False

        self.fluidColor = kwargs.get('fluid_color', '#41d94d')

        # DRAW PIPES
        if (pipe_top):
            xy = [(7 * width / 16.0, height / 4.0), (7 * width / 16.0, 0)]
            self.canvas.create_line(xy, width=1, fill='white')
            xy2 = [(9 * width / 16.0, height / 4.0), (9 * width / 16.0, 0)]
            self.canvas.create_line(xy2, width=1, fill='white')
        if (pipe_right):
            xy = [(width * (3 / 4.0), 7 * height / 16.0), (width, 7 * height / 16.0)]
            self.canvas.create_line(xy, width=1, fill='white')
            xy2 = [(width * (3 / 4.0), 9 * height / 16.0), (width, 9 * height / 16.0)]
            self.canvas.create_line(xy2, width=1, fill='white')
        if (line_3):
            xy = [(7 * width / 16.0, height * (3 / 4.0)), (7 * width / 16.0, height)]
            self.canvas.create_line(xy, width=1, fill='white')
            xy2 = [(9 * width / 16.0, height * (3 / 4.0)), (9 * width / 16.0, height)]
            self.canvas.create_line(xy2, width=1, fill='white')
        if (line_4):
            xy = [(width / 4.0, 7 * height / 16.0), (0, 7 * height / 16.0)]
            self.canvas.create_line(xy, width=1, fill='white')
            xy2 = [(width / 4.0, 9 * height / 16.0), (0, 9 * height / 16.0)]
            self.canvas.create_line(xy2, width=1, fill='white')

        # DRAW FLOW
        self.f1 = self.canvas.create_rectangle((7 * width / 16.0) + 1, 0, (9 * width / 16.0) - 1, (height / 4.0) - 1,
                                          fill='black', outline="")
        self.f2 = self.canvas.create_rectangle((3 * width / 4.0) + 1, (7 * height / 16.0) + 1, width,
                                          (9 * height / 16.0) - 1,
                                          fill='black', outline="")
        self.f3 = self.canvas.create_rectangle((7 * width / 16.0) + 1, (3 * height / 4.0) + 1, (9 * width / 16.0) - 1,
                                          height,
                                          fill='black', outline="")
        self.f4 = self.canvas.create_rectangle(0, (7 * height / 16.0) + 1, (width / 4.0) - 1, (9 * height / 16.0) - 1,
                                          fill='black', outline="")

    def setPipes(self, fill_1, fill_2, fill_3, fill_4):
        # absolute condition, True = Fluid color, False = black
        self.fill1 = fill_1
        self.fill2 = fill_2
        self.fill3 = fill_3
        self.fill4 = fill_4
        if (fill_1):
            self.canvas.itemconfig(self.f1, fill=self.fluidColor)
        else:
            self.canvas.itemconfig(self.f1, fill='black')
        if (fill_2):
            self.canvas.itemconfig(self.f2, fill=self.fluidColor)
        else:
            self.canvas.itemconfig(self.f2, fill='black')
        if (fill_3):
            self.canvas.itemconfig(self.f3, fill=self.fluidColor)
        else:
            self.canvas.itemconfig(self.f3, fill='black')
        if (fill_4):
            self.canvas.itemconfig(self.f4, fill=self.fluidColor)
        else:
            self.canvas.itemconfig(self.f4, fill='black')

    def setFill(self, fill_1, fill_2, fill_3, fill_4):
        # change color only if true
        if (fill_1):
            self.canvas.itemconfig(self.f1, fill=self.fluidColor)
        if (fill_2):
            self.canvas.itemconfig(self.f2, fill=self.fluidColor)
        if (fill_3):
            self.canvas.itemconfig(self.f3, fill=self.fluidColor)
        if (fill_4):
            self.canvas.itemconfig(self.f4, fill=self.fluidColor)

    def setNeighbors(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def getWidget(self):
        return self.canvas




class Solenoid(Component):
    def __init__(self, root, bg_color, num, width, height, pipe_top, pipe_right, line_3, line_4, **kwargs):
        Component.__init__(self, root, bg_color, width, height, pipe_top, pipe_right, line_3, line_4, fluid_color=kwargs.get('fluid_color', '#41d94d'))
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
                self.canvas.itemconfig(self.f1, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.f1, fill='black')
        if (self.inlet == 2):
            if(self.right is not None and self.right.getState()):
                self.canvas.itemconfig(self.f2, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.f2, fill='black')
        if (self.inlet == 3):
            if (self.bottom is not None and self.bottom.getState()):
                self.canvas.itemconfig(self.f3, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.f3, fill='black')
        if (self.inlet == 4):
            if (self.left is not None and self.left.getState()):
                self.canvas.itemconfig(self.f4, fill=self.fluidColor)
                inlet = True
            else:
                self.canvas.itemconfig(self.f4, fill='black')

        if(open):
            self.state = True
            self.canvas.itemconfig(self.fill, fill='#41d94d')
            if (self.outlet == 1):
                if(inlet):
                    self.canvas.itemconfig(self.f1, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.f1, fill='black')
            if (self.outlet == 2):
                if (inlet):
                    self.canvas.itemconfig(self.f2, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.f2, fill='black')
            if (self.outlet == 3):
                if (inlet):
                    self.canvas.itemconfig(self.f3, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.f3, fill='black')
            if (self.outlet == 4):
                if (inlet):
                    self.canvas.itemconfig(self.f4, fill=self.fluidColor)
                else:
                    self.canvas.itemconfig(self.f4, fill='black')
        else:
            self.state = False
            self.canvas.itemconfig(self.fill, fill = '#ab1f1f')
            if (self.outlet == 1):
                self.canvas.itemconfig(self.f1, fill='black')
            if (self.outlet == 2):
                self.canvas.itemconfig(self.f2, fill='black')
            if (self.outlet == 3):
                self.canvas.itemconfig(self.f3, fill='black')
            if (self.outlet == 4):
                self.canvas.itemconfig(self.f4, fill='black')




class Stepper(Component):

    def __init__(self, root, bg_color, width, height, pipe_top, pipe_right, line_3, line_4, **kwargs):
        Component.__init__(self, root, bg_color, width, height, pipe_top, pipe_right, line_3, line_4, fluid_color=kwargs.get('fluid_color', '#41d94d'))

        self.fill = self.canvas.create_rectangle((width/4.0), (height/4.0), (width*(3/4.0)), (height*(3/4.0)), fill='#ab1f1f')
        self.fillGreen = self.canvas.create_rectangle((width / 4.0), (height / 4.0), (width / 4.0), (height * (3 / 4.0)), fill='#41d94d')
        self.rect = self.canvas.create_rectangle(width/4.0, height/4.0, width*(3/4.0), height*(3/4.0), outline='white')

        self.percentage = self.canvas.create_text(width / 2.0, height / 2.0, font=("Arial", 10, 'bold'), fill="white", text="_ _ %")
        self.per = 0

    def setPercentage(self, p):
        self.per = p
        self.canvas.itemconfig(self.percentage, text=str(p)+' %')
        self.canvas.coords(self.fillGreen, (self.width / 4.0), (self.height / 4.0), (self.width / 4.0) + ((p/100.0)*self.width/2.0), (self.height * (3 / 4.0)))

    def getPercentage(self):
        return self.per




class Orifice(Component):

    def __init__(self, root, bg_color, width, height, pipe_top, pipe_right, line_3, line_4, **kwargs):

        Component.__init__(self, root, bg_color, width, height, pipe_top, pipe_right, line_3, line_4, fluid_color=kwargs.get('fluid_color', '#41d94d'))

        self.state = False

        self.rect = self.canvas.create_rectangle(width/4.0, height/4.0, width*(3/4.0), height*(3/4.0), outline='white')
        self.canvas.create_line((width / 4.0, height / 2.0), (3 * width / 4.0, height / 2.0), width=1, fill='white')
        self.beforeP = self.canvas.create_text(width / 2.0, 3 * height / 8.0, font=("Arial", 8, 'bold'), fill="white",
                                             text="B: __ Pa")
        self.afterP = self.canvas.create_text(width / 2.0, 5 * height / 8.0, font=("Arial", 8, 'bold'), fill="white",
                                         text="A: __ Pa")
        self.name = self.canvas.create_text(width/4.0, height/8.0, font=("Arial", 6, 'bold'), fill="white",
                                         text="Orifice")

    def setPipes(self, state):
        self.state = state
        if(state):
            if (self.pipe_top):
                self.canvas.itemconfig(self.f1, fill=self.fluidColor)
            if (self.pipe_right):
                self.canvas.itemconfig(self.f2, fill=self.fluidColor)
            if (self.line_3):
                self.canvas.itemconfig(self.f3, fill=self.fluidColor)
            if (self.line_4):
                self.canvas.itemconfig(self.f4, fill=self.fluidColor)
        else:
            if (self.pipe_top):
                self.canvas.itemconfig(self.f1, fill='black')
            if (self.pipe_right):
                self.canvas.itemconfig(self.f2, fill='black')
            if (self.line_3):
                self.canvas.itemconfig(self.f3, fill='black')
            if (self.line_4):
                self.canvas.itemconfig(self.f4, fill='black')

    def getState(self):
        return self.state

    def setValues(self, before, after):
        self.canvas.itemconfig(self.beforeP, text='B: ' + before + ' Pa')
        self.canvas.itemconfig(self.afterP, text='A: ' + after + ' Pa')




class PressureSensor(Component):

    def __init__(self, root, bg_color, width, height, pipe_top, pipe_right, line_3, line_4, **kwargs):

        Component.__init__(self, root, bg_color, width, height, pipe_top, pipe_right, line_3, line_4, fluid_color=kwargs.get('fluid_color', '#41d94d'))

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
                self.canvas.itemconfig(self.f1, fill=self.fluidColor)
            if (self.pipe_right):
                self.canvas.itemconfig(self.f2, fill=self.fluidColor)
            if (self.line_3):
                self.canvas.itemconfig(self.f3, fill=self.fluidColor)
            if (self.line_4):
                self.canvas.itemconfig(self.f4, fill=self.fluidColor)
        else:
            if (self.pipe_top):
                self.canvas.itemconfig(self.f1, fill='black')
            if (self.pipe_right):
                self.canvas.itemconfig(self.f2, fill='black')
            if (self.line_3):
                self.canvas.itemconfig(self.f3, fill='black')
            if (self.line_4):
                self.canvas.itemconfig(self.f4, fill='black')

    def getState(self):
        return self.state

    def setValues(self, pressure):
        self.canvas.itemconfig(self.p, text=pressure)




class TempSensor(Component):

    def __init__(self, root, bg_color, width, height, pipe_top, pipe_right, line_3, line_4, **kwargs):

        Component.__init__(self, root, bg_color, width, height, pipe_top, pipe_right, line_3, line_4, fluid_color=kwargs.get('fluid_color', '#41d94d'))

        self.state = False

        self.rect = self.canvas.create_oval(width / 4.0, height / 4.0, width * (3 / 4.0), height * (3 / 4.0),
                                            outline='white', width=1)
        self.p = self.canvas.create_text(width / 2.0, height / 2.0, font=("Arial", 8, 'bold'), fill="white",
                                             text="__ °C")
        self.name = self.canvas.create_text(width/4.0, height/8.0, font=("Arial", 6, 'bold'), fill="white",
                                         text="Temp\nSensor")

    def setPipes(self, state):
        self.state = state
        if(state):
            if (self.pipe_top):
                self.canvas.itemconfig(self.f1, fill=self.fluidColor)
            if (self.pipe_right):
                self.canvas.itemconfig(self.f2, fill=self.fluidColor)
            if (self.line_3):
                self.canvas.itemconfig(self.f3, fill=self.fluidColor)
            if (self.line_4):
                self.canvas.itemconfig(self.f4, fill=self.fluidColor)
        else:
            if (self.pipe_top):
                self.canvas.itemconfig(self.f1, fill='black')
            if (self.pipe_right):
                self.canvas.itemconfig(self.f2, fill='black')
            if (self.line_3):
                self.canvas.itemconfig(self.f3, fill='black')
            if (self.line_4):
                self.canvas.itemconfig(self.f4, fill='black')

    def getState(self):
        return self.state

    def setValues(self, pressure):
        self.canvas.itemconfig(self.p, text=pressure)




class Tank:

    def __init__(self, root, bg_color, title, fluidColor, width, height):
        padding = 15

        self.canvas = Canvas(root, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.width = width
        self.height = height

        self.top = None
        self.right = None
        self.bottom = None
        self.left = None

        self.rect = self.canvas.create_rectangle(width/4.0, 0, width*(3/4.0), height-1, outline='white')
        self.fill = self.canvas.create_rectangle((width/4.0) + 1, 50,width*(3/4.0)-1, height-2, fill=fluidColor)

        self.pressure = self.canvas.create_text(width / 2.0, (height / 2.0) - 1.25*padding, font=("Arial", 11, 'bold'), fill="white", text=title)
        self.pressure = self.canvas.create_text(width/2.0, (height/2.0), font=("Arial", 8), fill="white", text='psi')
        self.percentage = self.canvas.create_text(width/2.0, (height/2.0) + padding, font=("Arial", 8), fill="white", text='%')
        self.temperature = self.canvas.create_text(width/2.0, (height/2.0) + 2*padding, font=("Arial", 8), fill="white", text='tmp')


    def setTankLevel(self, percent):
        self.canvas.coords(self.fill, (self.width/4.0) + 1, self.height - ((percent/100.0)*self.height-2) - 2, self.width*(3/4.0)-1, self.height-2)
        self.canvas.itemconfig(self.percentage, text=str(percent) + " %")

    def setTankReadout(self, tmp, pressure):
        self.canvas.itemconfig(self.pressure, text=str(pressure) + ' psi')
        self.canvas.itemconfig(self.temperature, text=str(tmp) + ' °C')

    def setNeighbors(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def getWidget(self):
        return self.canvas




"""
The following class makes it simple to connect different GUI P&ID objects together with pipes.
The PIPE Class operates on five main parameters: line1, line2, line3, line4, fill

All 5 parameters are of the data type boolean and control the type of pipe and whether fluid is running through it
(respectively)

The booleans line# correspond to which side gets a pipe:
line1: 12:00
line2: 3:00
line3: 6:00
line4: 9:00

        ln1

  ln4    P    ln2

        ln3

By modulating these input parameters, any pipe can be designed to fit the GUI P&ID.

Additionally, all components are linked together with a singly linked list (which functions more as a map). This
allows for a traversal of the list to enable mass flow indicators on the GUI P&ID sketch.
"""

class Pipe:

    def __init__(self, root, bg_color, width, height, pipe_top, pipe_right, line_3, line_4, fluidColor, fill):
        self.canvas = Canvas(root, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.width = width
        self.height = height

        self.line1 = pipe_top
        self.line2 = pipe_right
        self.line3 = line_3
        self.line4 = line_4

        self.top = None
        self.right = None
        self.bottom = None
        self.left = None

        self.state = False
        self.fluidColor = fluidColor


        # DRAW PIPES
        if (fill):
            self.f0 = self.canvas.create_rectangle(7 * width / 16.0, 7 * height / 16.0, 9 * width / 16.0, 9 * height / 16.0,
                                              fill=fluidColor)
        else:
            self.f0 = self.canvas.create_rectangle(7 * width / 16.0, 7 * height / 16.0, 9 * width / 16.0, 9 * height / 16.0,
                                              fill='black')

        if (pipe_top):
            xy = [(7 * width / 16.0, 0), (7 * width / 16.0, 7 * height / 16.0)]
            self.canvas.create_line(xy, width=1, fill='white')
            xy2 = [(9 * width / 16.0, 0), (9 * width / 16.0, 7 * height / 16.0)]
            self.canvas.create_line(xy2, width=1, fill='white')
            if (fill):
                self.f1 = self.canvas.create_rectangle((7 * width / 16.0) + 1, 0, (9 * width / 16.0) - 1,
                                                  (7 * height / 16.0) + 1,
                                                  fill=fluidColor, outline="")
            else:
                self.f1 = self.canvas.create_rectangle((7 * width / 16.0) + 1, 0, (9 * width / 16.0) - 1,
                                                  (7 * height / 16.0) + 1,
                                                  fill='black', outline="")
        else:
            xy = [(7 * width / 16.0, 7 * height / 16.0), (9 * width / 16.0, 7 * height / 16.0)]
            self.canvas.create_line(xy, width=1, fill='white')
        if (pipe_right):
            xy = [(9 * width / 16.0, 7 * height / 16.0), (width, 7 * height / 16.0)]
            self.canvas.create_line(xy, width=1, fill='white')
            xy2 = [(9 * width / 16.0, 9 * height / 16.0), (width, 9 * height / 16.0)]
            self.canvas.create_line(xy2, width=1, fill='white')
            if (fill):
                self.f2 = self.canvas.create_rectangle(9 * width / 16.0, (7 * height / 16.0) + 1, width,
                                                  (9 * height / 16.0) - 1,
                                                  fill=fluidColor, outline="")
            else:
                self.f2 = self.canvas.create_rectangle(9 * width / 16.0, (7 * height / 16.0) + 1, width,
                                                  (9 * height / 16.0) - 1,
                                                  fill='black', outline="")
        else:
            xy = [(9 * width / 16.0, 7 * height / 16.0), (9 * width / 16.0, 9 * height / 16.0)]
            self.canvas.create_line(xy, width=1, fill='white')
        if (line_3):
            xy = [(7 * width / 16.0, 9 * height / 16.0), (7 * width / 16.0, height)]
            self.canvas.create_line(xy, width=1, fill='white')
            xy2 = [(9 * width / 16.0, 9 * height / 16.0), (9 * width / 16.0, height)]
            self.canvas.create_line(xy2, width=1, fill='white')
            if (fill):
                self.f3 = self.canvas.create_rectangle((7 * width / 16.0) + 1, 9 * height / 16.0, (9 * width / 16.0) - 1,
                                                  height,
                                                  fill=fluidColor, outline="")
            else:
                self.f3 = self.canvas.create_rectangle((7 * width / 16.0) + 1, 9 * height / 16.0, (9 * width / 16.0) - 1,
                                                  height,
                                                  fill='black', outline="")
        else:
            xy = [(7 * width / 16.0, 9 * height / 16.0), (9 * width / 16.0, 9 * height / 16.0)]
            self.canvas.create_line(xy, width=1, fill='white')
        if (line_4):
            xy = [(0, 7 * height / 16.0), (7 * width / 16.0, 7 * height / 16.0)]
            self.canvas.create_line(xy, width=1, fill='white')
            xy2 = [(0, 9 * height / 16.0), (7 * width / 16.0, 9 * height / 16.0)]
            self.canvas.create_line(xy2, width=1, fill='white')
            if (fill):
                self.f4 = self.canvas.create_rectangle(0, (7 * height / 16.0) + 1, (7 * width / 16.0) + 1,
                                                  (9 * height / 16.0) - 1,
                                                  fill=fluidColor, outline="")
            else:
                self.f4 = self.canvas.create_rectangle(0, (7 * height / 16.0) + 1, (7 * width / 16.0) + 1,
                                                  (9 * height / 16.0) - 1,
                                                  fill='black', outline="")
        else:
            xy = [(7 * width / 16.0, 7 * height / 16.0), (7 * width / 16.0, 9 * height / 16.0)]
            self.canvas.create_line(xy, width=1, fill='white')

    def setNeighbors(self, top, right, bottom, left):
        # function used to populate map to establish relations between this pipe and components around it
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def setState(self, fluid):
        self.state = fluid
        if (fluid):
            self.canvas.itemconfig(self.f0, fill=self.fluidColor)
            if (self.line1):
                self.canvas.itemconfig(self.f1, fill=self.fluidColor)
            if (self.line2):
                self.canvas.itemconfig(self.f2, fill=self.fluidColor)
            if (self.line3):
                self.canvas.itemconfig(self.f3, fill=self.fluidColor)
            if (self.line4):
                self.canvas.itemconfig(self.f4, fill=self.fluidColor)
        else:
            self.canvas.itemconfig(self.f0, fill='black')
            if (self.line1):
                self.canvas.itemconfig(self.f1, fill='black')
            if (self.line2):
                self.canvas.itemconfig(self.f2, fill='black')
            if (self.line3):
                self.canvas.itemconfig(self.f3, fill='black')
            if (self.line4):
                self.canvas.itemconfig(self.f4, fill='black')

    def getState(self):
        return self.state

    def getWidget(self):
        return self.canvas




class Nozzle:

    def __init__(self, root, bg_color, width, height):
        padding = 25

        self.top = None
        self.right = None
        self.bottom = None
        self.left = None

        self.canvas = Canvas(root, width=width, height=height, bg=bg_color, highlightthickness=0)
        self.width = width
        self.height = height

        self.plot = []
        self.plot.append((1, 1))
        self.plot.append((width - 1, 1))
        self.plot.append((width - 1, height * 0.1))
        self.plot.append((0.9 * width, height * 0.1))
        self.plot.append((0.9 * width, height * 0.7))
        self.plot.append((0.6 * width, height * 0.9))
        self.plot.append((0.7*width, height-1))
        self.plot.append((0.3*width, height-1))
        self.plot.append((0.4 * width, height * 0.9))
        self.plot.append((0.1 * width, height * 0.7))
        self.plot.append((0.1 * width, height * 0.1))
        self.plot.append((1, height * 0.1))

        self.base = self.canvas.create_polygon(self.plot, outline='white')

        self.thrust = self.canvas.create_text(width/2.0, (height/2.0) - padding, font=("Arial", 10), fill="white", text='thrust')
        self.pressure = self.canvas.create_text(width/2.0, height/2.0, font=("Arial", 10), fill="white", text='pressure')


    def setNeighbors(self, top, right, bottom, left):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    def getWidget(self):
        return self.canvas

    def setNozzleReadout(self, thrust, pressure):
        self.canvas.itemconfig(self.thrust, text='LC: ' + str(thrust) + ' N')
        self.canvas.itemconfig(self.pressure, text='PT: ' + str(pressure) + ' psi')

