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
import tkinter as tk
from   serial    import SerialException
from   mttkinter import mtTkinter
from   PIL       import Image, ImageTk


###############################################################
# Project Modules                                             #
###############################################################
import gauge
import valve
import PandID
import sequence


###############################################################
# Main application entry point                                #
###############################################################
if __name__ == '__main__':

	###########################################################
	# Global variables                                        #
	###########################################################
    global root                 # Main window object
    global plumbing             # Engine schematic object
    global off_button           # All valves off button
    global USB_connection_label # USB connection widget objects
    global switch1              # valve button objects
    global switch2          
    global switch3 
    global switch4 
    global switch5 
    global switch6
    global switch7 
    global switch8 
    global valve_button_row1    # valve button row frames
    global valve_button_row2
    global valve_button_row3
    global valve_button_row4
    global gauge1               # sensor gauge objects
    global gauge2    
    global gauge3 
    global gauge4           


	###########################################################
	# Local variables                                         #
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
    root.geometry("900x1000")

	# Program icon
    SDRlogo = tk.PhotoImage(file='images/SDRLogo5.png')
    SDRImage = Image.open("images/SDRlogont2.png")
    SDRImage = SDRImage.resize((280,250),Image.Resampling.LANCZOS)
    SDR = ImageTk.PhotoImage(SDRImage)
    root.iconphoto(True,SDRlogo)

    # Valve button row frames
    valve_button_row1   = tk.Frame(root,       
                                   bg='black') 

    valve_button_row2   = tk.Frame(root,       
                                   bg='black') 

    valve_button_row3   = tk.Frame(root,       
                                   bg='black') 

    valve_button_row4   = tk.Frame(root,       
                                   bg='black') 

	# Sequence button frames
    sequence_frame_row1 = tk.Frame(root,
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
    main_window_title     = tk.Label(root, 
                                    text="Engine Dashboard", 
                                    bg="black", 
                                    fg="white", 
                                    font="Arial 30")

    # USB connection label
    USB_connection_label = tk.Label(root, 
                                    text='DISCONNECTED ', 
                                    bg="black", 
                                    fg="#ed3b3b", 
                                    font="Arial 14")


	# Valve buttons
    switch1 = valve.Buttons(valve_button_row1,
                                  "Relay 1", 
                                  plumbing.one)
    switch2 = valve.Buttons(valve_button_row2,
                                  "Relay 2", 
                                  plumbing.two)
    switch3 = valve.Buttons(valve_button_row3,
                                  "Relay 3", 
                                  plumbing.three)
    switch4 = valve.Buttons(valve_button_row4,
                                  "Relay 4", 
                                  plumbing.four)
    switch5 = valve.Buttons(valve_button_row1,
                                  "Relay 5", 
                                  plumbing.five)
    switch6 = valve.Buttons(valve_button_row2,
                                  "Relay 6", 
                                  plumbing.six)
    switch7 = valve.BV_button(valve_button_row3,
                                  "Relay 7")
    switch8 = valve.BV_button(valve_button_row4,
                                  "Relay 8")

	# Startup button
    startup_button = tk.Button(sequence_frame_row1, 
                               text="STARTUP", 
                               padx=40, 
                               pady=10, 
                               font="Verdana 14", 
                               bg="black", 
                               fg="white", 
                               command=sequence.startup,
                               activebackground="white",
                               relief="solid",
							   highlightthickness=2,
                               borderwidth=5)

	# All valves off button
    off_button    = tk.Button(sequence_frame_row1, 
                              text="ALL OFF", 
                              padx=45, 
                              pady=10, 
                              font="Verdana 14", 
                              bg="black", 
                              fg="white", 
                              command=sequence.allOff,
                              relief="solid",
						      highlightthickness=2,
                              borderwidth=5,
                              activebackground="white")

	# Sensor gauges
    gauge1 = gauge.gauge(gauge_frame_row1, 'black', 5)
    gauge1.setText("Nan", "A0")
    gauge2 = gauge.gauge(gauge_frame_row1, 'black', 5)
    gauge2.setText("Nan", "A1")
    gauge3 = gauge.gauge(gauge_frame_row1, 'black', 5)
    gauge3.setText("Nan", "A2")
    gauge4 = gauge.gauge(gauge_frame_row1, 'black', 5)
    gauge4.setText("Nan", "A3")
    gauge5 = gauge.gauge(gauge_frame_row2, 'black', 5)
    gauge5.setText("Nan", "A0")
    gauge6 = gauge.gauge(gauge_frame_row2, 'black', 5)
    gauge6.setText("Nan", "A1")
    gauge7 = gauge.gauge(gauge_frame_row2, 'black', 5)
    gauge7.setText("Nan", "A2")
    gauge8 = gauge.gauge(gauge_frame_row2, 'black', 5)
    gauge8.setText("Nan", "A3")


	###########################################################
	# Draw initial window                                     #
	###########################################################

	# Main window title
    main_window_title.pack(pady=40)

	# USB connection label
    USB_connection_label.pack()

	# Valve buttons
    valve_button_row1.pack()
    valve_button_row2.pack()
    valve_button_row3.pack()
    valve_button_row4.pack()

	# Sequence button frames
    sequence_frame_row1.pack()

	# Sequence frames
    startup_button.pack(side="left" , padx=60, pady=30)
    off_button.pack(    side="right", padx=60, pady=30)

	# Gauge frame rows 
    gauge_frame_row1.pack()
    gauge_frame_row2.pack()

	# Gauges
    gauge1.getWidget().pack(side= "left"   )
    gauge2.getWidget().pack(side= "left"   )
    gauge3.getWidget().pack(side= "right"  )
    gauge4.getWidget().pack(side= "right"  )
    gauge5.getWidget().pack(side= "left"   )
    gauge6.getWidget().pack(side= "left"   )
    gauge7.getWidget().pack(side= "right"  )
    gauge8.getWidget().pack(side= "right"  )


	###########################################################
	# Main Program Loop                                       #
	###########################################################
    prevCon = True
    while True:
		# Update USB connection label
        USB_connection_label.configure(text='DISCONNECTED ',
                                       fg  ="#ed3b3b")

		# Update sensor gauge readings
        gauge1.setText("Nan", "A0")
        gauge2.setText("Nan", "A1")
        gauge3.setText("Nan", "A2")
        gauge4.setText("Nan", "A3")
        gauge5.setText("Nan", "A4")
        gauge6.setText("Nan", "A5")
        gauge7.setText("Nan", "A6")
        gauge8.setText("Nan", "A7")

		# Update engine schematic
        plumbing.updatePipeStatus()

		# Draw to main window
        root.update()

		# Draw to plumbing window
        plumbing.getWindow().update()

###############################################################
# END OF FILE                                                 #
###############################################################
