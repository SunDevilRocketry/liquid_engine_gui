###############################################################
#                                                             #
# main.py -- main interface program for SDR's liquid engine   #
#                                                             #
# Author: Nitish Chennoju, Colton Acosta                      #
# Date: 6/12/2022                                             #
# Sun Devil Rocketry Avionics                                 #
#                                                             #
###############################################################


###############################################################
# Developers                                                  #
###############################################################
__author__ =   "Nitish Chennoju"
__credits__ = ["Colton Acosta",
               "Katie Herrington",
               "Ian Chandra"]


###############################################################
# Standard Imports                                            #
###############################################################
import threading
import time
import serial
import serial.tools.list_ports
from serial import SerialException
import tkinter as tk
from mttkinter import mtTkinter


###############################################################
# Project Modules                                             #
###############################################################
import gauge
import RelaySwitch
import PandID
import sequence


###############################################################
# Main application entry point                                #
###############################################################
if __name__ == '__main__':

	###########################################################
	# Main application global variables                       #
	###########################################################
    global root, off, plumbing, arduinoSwitchbox # misc
    global connectionLabel, prevCon # serial connections
    global switch1, switch2, switch3, switch4 # switch objects
    global switch5, switch6, switch7, switch8 
    global a, b, c, d # tkinter window rows
    global g1, g2, g3, g4 # gauge objects


	###########################################################
	# Main application local variables                        #
	###########################################################
    pad = 10 # Spacing constants within GUI
    gridLen = 85


	###########################################################
	# Object and windows initialization                       #
	###########################################################

    #ACTION HANDLER THREAD (checks for startup button press)
    thread = threading.Thread(target=sequence.actionHandler)
    thread.start()

    # P&ID diagram window
    plumbing = PandID.Liquid_Engine_Plumbing(gridLen)  

    # root window
    root = tk.Tk(mt_debug = 1)
    root.title("Engine Dashboard")
    root.configure(background="black")
    tk.Label(root, 
             text="Engine Dashboard", 
             bg="black", 
             fg="white", 
             font="Arial 30").pack(pady=40)

    # GET ARDUINO STATUS / Update on GUI connection label
    connectionLabel = tk.Label(root, 
                               text='DISCONNECTED ', 
                               bg="black", 
                               fg="#ed3b3b", 
                               font="Arial 14")
    connectionLabel.pack()

    # Solenoid Switches
    a = tk.Frame(root, bg='black')  # represents tow 1
    b = tk.Frame(root, bg='black')  # represents tow 2
    c = tk.Frame(root, bg='black')  # represents tow 3
    d = tk.Frame(root, bg='black')  # represents tow 4
    switch1 = RelaySwitch.Buttons(a,"Relay 1", plumbing.one)
    switch2 = RelaySwitch.Buttons(b,"Relay 2", plumbing.two)
    switch3 = RelaySwitch.Buttons(c,"Relay 3", plumbing.three)
    switch4 = RelaySwitch.Buttons(d,"Relay 4", plumbing.four)
    switch5 = RelaySwitch.Buttons(a,"Relay 5", plumbing.five)
    switch6 = RelaySwitch.Buttons(b,"Relay 6", plumbing.six)
    a.pack()
    b.pack()
    c.pack()
    d.pack()

    g = tk.Frame(root)
    h = tk.Frame(root)

	# Startup button
    s = tk.Button(root, 
                  text="STARTUP", 
                  padx=40, 
                  pady=10, 
                  font="Verdana 14", 
                  bg="yellow", 
                  command=sequence.startup,
                  activebackground="yellow")
    s.pack(pady=pad)

	# All off button
    off = tk.Button(root, 
                    text="All OFF", 
                    padx=30, 
                    pady=10, 
                    font="Verdana 14", 
                    bg="RED", 
                    command=sequence.allOff,
                    activebackground="RED")
    off.pack(pady=pad)

	# Sensor gauges
    g1 = gauge.gauge(g, 'black', 5)
    g1.setText("Nan", "A0")
    g1.getWidget().pack(side="left")
    g2 = gauge.gauge(g, 'black', 5)
    g2.setText("Nan", "A1")
    g2.getWidget().pack(side="left")
    g3 = gauge.gauge(h, 'black', 5)
    g3.setText("Nan", "A2")
    g3.getWidget().pack(side="left")
    g4 = gauge.gauge(h, 'black', 5)
    g4.setText("Nan", "A3")
    g4.getWidget().pack(side="right")
    g.pack()
    h.pack()


	###########################################################
	# Main Program Loop                                       #
	###########################################################
    prevCon = True
    while True:
        connectionLabel.configure(text='DISCONNECTED ',
                                  fg="#ed3b3b")
        g1.setText("Nan", "A0")
        g2.setText("Nan", "A1")
        g3.setText("Nan", "A2")
        g4.setText("Nan", "A3")
        prevCon = False

        plumbing.updatePipeStatus()

        root.update()
        plumbing.getWindow().update()

###############################################################
# END OF FILE                                                 #
###############################################################
