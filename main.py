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
    global root                     # Main window object
    global plumbing                 # Engine schematic object
    global off_button               # All valves off button 
                                    # button
    global connectionLabel          # Label widget objects
    global switch1, switch2         # valve button objects 
    global switch3, switch4 
    global switch5, switch6
    global switch7, switch8 
    global valve_button_row1        # valve button row frames
    global valve_button_row2
    global valve_button_row3
    global valve_button_row4
    global gauge1, gauge2           # sensor gauge objects
    global gauge3, gauge4           


	###########################################################
	# Main application local variables                        #
	###########################################################
    pad = 10 # Spacing constants within GUI
    gridLen = 85


	###########################################################
	# Window frames                                           #
	###########################################################

	# root window
    root = tk.Tk(mt_debug = 1)         
    root.title("Engine Dashboard")
    root.configure(background="black")

    # Valve button row frames
    valve_button_row1 = tk.Frame(root,       
                                 bg='black') 

    valve_button_row2 = tk.Frame(root,       
                                 bg='black') 

    valve_button_row3 = tk.Frame(root,       
                                 bg='black') 

    valve_button_row4 = tk.Frame(root,       
                                 bg='black') 

	# Gauge row frames
    gauge_frame_row1 = tk.Frame(root)
    gauge_frame_row2 = tk.Frame(root)

	###########################################################
	# Widget initializations                                  #
	###########################################################

    #ACTION HANDLER THREAD (checks for startup button press)
    thread = threading.Thread(target=sequence.actionHandler)
    thread.start()

    # P&ID diagram window
    plumbing = PandID.Liquid_Engine_Plumbing(gridLen)  

	# Main window label
    main_window_title = tk.Label(root, 
                                 text="Engine Dashboard", 
                                 bg="black", 
                                 fg="white", 
                                 font="Arial 30")

    # USB connection label
    connectionLabel = tk.Label(root, 
                               text='DISCONNECTED ', 
                               bg="black", 
                               fg="#ed3b3b", 
                               font="Arial 14")


	# Solenoid buttons
    switch1 = RelaySwitch.Buttons(valve_button_row1,
                                  "Relay 1", 
                                  plumbing.one)
    switch2 = RelaySwitch.Buttons(valve_button_row2,
                                  "Relay 2", 
                                  plumbing.two)
    switch3 = RelaySwitch.Buttons(valve_button_row3,
                                  "Relay 3", 
                                  plumbing.three)
    switch4 = RelaySwitch.Buttons(valve_button_row4,
                                  "Relay 4", 
                                  plumbing.four)
    switch5 = RelaySwitch.Buttons(valve_button_row1,
                                  "Relay 5", 
                                  plumbing.five)
    switch6 = RelaySwitch.Buttons(valve_button_row2,
                                  "Relay 6", 
                                  plumbing.six)


	# Startup button
    startup_button = tk.Button(root, 
                               text="STARTUP", 
                               padx=40, 
                               pady=10, 
                               font="Verdana 14", 
                               bg="yellow", 
                               command=sequence.startup,
                               activebackground="yellow")

	# All valves off button
    off_button = tk.Button(root, 
                           text="All OFF", 
                           padx=30, 
                           pady=10, 
                           font="Verdana 14", 
                           bg="RED", 
                           command=sequence.allOff,
                           activebackground="RED")

	# Sensor gauges
    gauge1 = gauge.gauge(gauge_frame_row1, 'black', 5)
    gauge1.setText("Nan", "A0")
    gauge2 = gauge.gauge(gauge_frame_row1, 'black', 5)
    gauge2.setText("Nan", "A1")
    gauge3 = gauge.gauge(gauge_frame_row2, 'black', 5)
    gauge3.setText("Nan", "A2")
    gauge3.getWidget().pack(side="left")
    gauge4 = gauge.gauge(gauge_frame_row2, 'black', 5)
    gauge4.setText("Nan", "A3")

	###########################################################
	# Initial window draw                                     #
	###########################################################

	# Main window title
    main_window_title.pack(pady=40)

	# USB connection label
    connectionLabel.pack()

	# Valve buttons
    valve_button_row1.pack()
    valve_button_row2.pack()
    valve_button_row3.pack()
    valve_button_row4.pack()

	# Startup button
    startup_button.pack(pady=pad)

	# All valves off button 
    off_button.pack(pady=pad)

	# Gauge frame rows 
    gauge_frame_row1.pack()
    gauge_frame_row2.pack()

	# Gauges
    gauge1.getWidget().pack(side= "left"  )
    gauge2.getWidget().pack(side= "right" )
    gauge3.getWidget().pack(side= "left"  )
    gauge4.getWidget().pack(side= "right" )


	###########################################################
	# Main Program Loop                                       #
	###########################################################
    prevCon = True
    while True:
		# Update USB connection label
        connectionLabel.configure(text='DISCONNECTED ',
                                  fg="#ed3b3b")

		# Updated sensor gauge readings
        gauge1.setText("Nan", "A0")
        gauge2.setText("Nan", "A1")
        gauge3.setText("Nan", "A2")
        gauge4.setText("Nan", "A3")

		# Update engine schematic
        plumbing.updatePipeStatus()

		# Draw to main window
        root.update()

		# Draw to plumbing window
        plumbing.getWindow().update()

###############################################################
# END OF FILE                                                 #
###############################################################
