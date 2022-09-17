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
__author__  =  "Nitish Chennoju"
__credits__ = ["Colton Acosta"   ,
               "Katie Herrington",
               "Ian Chandra"      ]


###############################################################
# Standard Imports                                            #
###############################################################
import threading
import time
import os
import sys
import serial
import serial.tools.list_ports
import tkinter as tk

from tkinter  import ttk
from serial   import SerialException
from PIL      import Image, ImageTk


###############################################################
# Project Modules                                             #
###############################################################

# Setup path 
sys.path.insert(0, './plumbing')

# Imports
import solenoid
import gauge          as SDR_gauge
import valve          as SDR_valve
import engine_display as SDR_engine_display
import sequence       as SDR_sequence


###############################################################
# Callbacks                                                   #
###############################################################

# Close all GUI windows
def close_window_callback():
    global exitFlag
    root.destroy()
    plumbing.win.destroy()
    exitFlag = True


###############################################################
#                                                             #
# PROCEDURE:                                                  #
# 		adc_readout_to_voltage                                #
#                                                             #
# DESCRIPTION:                                                #
# 		displays a general software failure error message     #
#                                                             #
###############################################################
def adc_readout_to_voltage( 
                          readout, # ADC readout
                          num_bits # number of bits in ADC readout
                          ):
	voltage_step = 3.3/float(2**(num_bits))
	return readout*voltage_step 


###############################################################
#                                                             #
# OBJECT:                                                     #
# 		serialData                                            #
#                                                             #
# DESCRIPTION:                                                #
# 		serial port user API and handler for passing data     #
#       between command functions                             #
#                                                             #
###############################################################
class serialData:
    def __init__(self):
        self.baudrate            = None
        self.comport             = None
        self.timeout             = None
        self.serialObj           = serial.Serial()
        self.config_status       = False 
        self.controller          = None
        self.flash_write_enabled = False 

    # Initialize Serial Port
    def initComport(self, baudrate, comport, timeout):
        self.baudrate = baudrate 
        self.comport = comport 
        self.timeout = timeout 
        self.serialObj.baudrate = self.baudrate
        self.serialObj.port = self.comport
        self.serialObj.timeout = self.timeout
        self.config_status = True

    # Configure Serial port from class attributes
    def configComport(self):
        self.serialObj.baudrate = self.baudrate
        self.serialObj.port = self.comport
        self.serialObj.timeout = self.timeout

    # Open the serial port
    # returns a boolean variable indicating whether the port
    # connection was sucessful
    def openComport(self):

        # Ensure serial port has been properly configured 
        if(not self.config_status):
            print("Error: Cannot open serial port. Serial " +
                  "port has not been properly configured")
            return False

        # open port
        self.serialObj.open()
        return True

    # Close the serial port
    # Returns a boolean value indicating whether the port connection was 
    # successfully closed
    def closeComport(self):
        # check that the serial port is open
        if (not self.serialObj.is_open):
            print("No open serial port detected")
            return False
        else:
            self.serialObj.close()
            return True

	# Check if serial port is active
    def is_active(self):
        return self.serialObj.is_open

	# List available serial port connections
    def list_ports(self):
	    available_ports = serial.tools.list_ports.comports()
	    available_port_names = []
	    for port in available_ports:
		    available_port_names.append(port.device)
	    return available_port_names

    # Write a single Byte to the serial port
    def sendByte(self, byte):
        if (not self.serialObj.is_open):
            print("Error: Could not transmit byte over serial port. No active" \
                   +"serial port connection")
        else:
            self.serialObj.write(byte)

    # Write an array of bytes to the serial port 
    def sendBytes(self, byte_array):
        if (not self.serialObj.is_open):
            print("Error: Could not transmit byte over serial port. No active" \
                   +"serial port connection")
        else:
            for byte in byte_array:
                self.serialObj.write(byte)

    # Read a single Byte from the serial port
    def readByte(self):
        if (not self.serialObj.is_open):
            print("Error: Could not read byte from serial port. No active" \
                   +"serial port connection")
        else:
             return self.serialObj.read()

	# Set the SDR controller to enable board-specific commands
    def set_SDR_controller(self, controller_name):
        self.controller = controller_name

	# Reset the SDR controller to disable board-specific commands
    def reset_SDR_controller(self):
        self.controller = None


###############################################################
# Main application entry point                                #
###############################################################
if __name__ == '__main__':

	###########################################################
	# Global variables                                        #
	###########################################################

	# Declarations
    global exitFlag             # Flag set when window closes        

    # Initializations
    exitFlag = False

	# Serial Port Object
    serObj = serialData()
    serObj.initComport(9600, '/dev/ttyUSB0', 1)
    serObj.openComport()


	###########################################################
	# Local variables                                         #
	###########################################################

    # Spacing constants within GUI
    pad     = 10 
    gridLen = 85


	###########################################################
	# Window frames                                           #
	###########################################################

	# root window
    root = tk.Tk()         
    root.title("Engine Dashboard")
    root.configure(
                  background="black",
                  borderwidth=10
                  )
    root.geometry("900x1000")
    root.protocol(
                 "WM_DELETE_WINDOW",
                 close_window_callback
                 )

	# Program icon
    SDRlogo  = tk.PhotoImage(file='images/SDRLogo5.png')
    SDRImage = Image.open("images/SDRlogont2.png")
    SDRImage = SDRImage.resize(
                              (int(0.8*140),int(0.8*125)),
                              Image.Resampling.LANCZOS
                              )
    SDR = ImageTk.PhotoImage(SDRImage)
    root.iconphoto(True, SDRlogo)

    # Logo and dashboard label frame
    main_title_frame    = tk.Frame(
                                  root,
                                  bg = 'black'
                                  )

    # Valve button row frames
    valve_button_row1   = tk.Frame(
                                  root,       
                                  bg = 'black'
                                  ) 

    valve_button_row2   = tk.Frame(
                                  root,       
                                  bg = 'black'
                                  ) 

    valve_button_row3   = tk.Frame(
                                  root,       
                                  bg = 'black'
                                  ) 

    valve_button_row4   = tk.Frame(
                                  root,       
                                  bg = 'black'
                                  ) 

	# Sequence button frames
    sequence_frame_row1 = tk.Frame(
                                  root,
								  bg='black'
                                  )

	# Gauge row frames
    gauge_frame_row1    = tk.Frame(
                                  root, 
                                  bg='black'
                                  )

    gauge_frame_row2    = tk.Frame(
                                  root, 
                                  bg='black'
                                  )


	###########################################################
	# Widget initializations                                  #
	###########################################################

    # P&ID diagram window
    plumbing = SDR_engine_display.Engine_Display(gridLen)  

    # SDR logo
    SDRlabel =                tk.Label(
                                      main_title_frame,
                                      image = SDR, 
                                      bg = 'black'
                                      )

	# Main window label
    main_window_title =       tk.Label(
                                      main_title_frame, 
                                      text="Engine Dashboard", 
                                      bg="black", 
                                      fg="white", 
                                      font="Arial 30"
                                      )

	# Valve buttons
    solenoid1_buttons = SDR_valve.Buttons(
                                     valve_button_row1,
                                     "LOX Pressurization (1)", 
                                     plumbing.one
                                     )

    solenoid2_buttons = SDR_valve.Buttons(
                                     valve_button_row2,
                                     "Kerosene Pressurization (2)", 
                                     plumbing.two
                                     )

    solenoid3_buttons = SDR_valve.Buttons(
                                     valve_button_row3,
                                     "LOX Vent (2)", 
                                     plumbing.three
                                     )

    solenoid4_buttons = SDR_valve.Buttons(
                                     valve_button_row4,
                                     "Kerosene Vent (4)", 
                                     plumbing.four
                                     )

    solenoid5_buttons = SDR_valve.Buttons(
                                     valve_button_row1,
                                     "LOX Purge (5)", 
                                     plumbing.five
                                     )

    solenoid6_buttons = SDR_valve.Buttons(
                                     valve_button_row2,
                                     "Kerosene Purge (6)", 
                                     plumbing.six
                                     )

    ball_valve1_buttons = SDR_valve.Buttons(
                                    valve_button_row3,
                                    "LOX Main Valve"
                                    )

    ball_valve2_buttons = SDR_valve.Buttons(
                                    valve_button_row4,
                                    "Kerosene Main Valve"
                                    )

	# Startup button
    startup_button =    tk.Button(
                                 sequence_frame_row1, 
                                 text="STARTUP", 
                                 padx=40, 
                                 pady=10, 
                                 font="Verdana 14", 
                                 bg="black", 
                                 fg="white", 
                                 command=SDR_sequence.startup,
                                 activebackground="white",
                                 relief="solid",
							     highlightthickness=2,
                                 borderwidth=5
                                 )

	# All valves off button
    off_button    =     tk.Button(
                                 sequence_frame_row1, 
                                 text="ALL OFF", 
                                 padx=45, 
                                 pady=10, 
                                 font="Verdana 14", 
                                 bg="black", 
                                 fg="white", 
                                 command=SDR_sequence.allOff,
                                 relief="solid",
						         highlightthickness=2,
                                 borderwidth=5,
                                 activebackground="white"
                                 )

	# Sensor gauges
    gauge1 =      SDR_gauge.gauge(
                                 gauge_frame_row1, 
                                 background = 'black',
                                 max_sensor_val = 1000
                                 )

    gauge2 =      SDR_gauge.gauge(
                                 gauge_frame_row1, 
                                 background = 'black',
                                 max_sensor_val =  1000
                                 )

    gauge3 =      SDR_gauge.gauge(
                                 gauge_frame_row1, 
                                 background = 'black',
                                 max_sensor_val =  1000
                                 )

    gauge4 =      SDR_gauge.gauge(
                                 gauge_frame_row1, 
                                 background = 'black', 
                                 max_sensor_val = 1000
                                 )

    gauge5 =      SDR_gauge.gauge(
                                 gauge_frame_row2, 
                                 background = 'black', 
                                 max_sensor_val = 1000 
                                 )

    gauge6 =      SDR_gauge.gauge(
                                 gauge_frame_row2, 
                                 background = 'black', 
                                 max_sensor_val = 1000 
                                 )

    gauge7 =      SDR_gauge.gauge(
                                 gauge_frame_row2, 
                                 background = 'black', 
                                 max_sensor_val = 1000
                                 )

    gauge8 =      SDR_gauge.gauge(
                                 gauge_frame_row2, 
                                 background = 'black', 
                                 max_sensor_val = 1000
                                 )

    gauge1.setText("Nan", "Fuel Tank Pressure"     )
    gauge2.setText("Nan", "Fuel Flow Rate"         )
    gauge3.setText("Nan", "Fuel Injection Pressure")
    gauge4.setText("Nan", "Thrust"                 )
    gauge5.setText("Nan", "LOX Pressure"           )
    gauge6.setText("Nan", "LOX Flow Rate"          )
    gauge7.setText("Nan", "Engine Pressure"        )
    gauge8.setText("Nan", "LOX Temperature"        )


	###########################################################
	# Draw initial window                                     #
	###########################################################

	# Main window title
    main_title_frame.pack()
    SDRlabel.pack(side='left', padx=30)
    main_window_title.pack(pady=30, side='right')

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
    gauge1.getWidget().pack(side='left')
    gauge2.getWidget().pack(side='left')
    gauge3.getWidget().pack(side='left')
    gauge4.getWidget().pack(side='left')
    gauge5.getWidget().pack(side='left')
    gauge6.getWidget().pack(side='left')
    gauge7.getWidget().pack(side='left')
    gauge8.getWidget().pack(side='left')


	###########################################################
	# Main Program Loop                                       #
	###########################################################
    prevCon = True
    while (not exitFlag):
        try:
			# Send request for reading
            serObj.sendByte(b'\x34')

			# Get Readings
            pt_readout_bytes = []
            for i in range( 4 ):
                pt_readout_bytes.append( serObj.readByte() )

            # Convert from bytes to voltage
            sensor_val = 0
            for j in range(4): # Hex to integer conversion
                sensor_val += ( int.from_bytes( pt_readout_bytes[j], 'big') << 8*(3-j) )
            sensor_val = adc_readout_to_voltage( sensor_val, 16 )

			# Convert from voltage to psi
            psi_readout = sensor_val*(1000.0/3.3)

			# Format string to be printed to GUI
            psi_readout_string = "{:.1f} psi".format( psi_readout )

		    # Update sensor gauge readings
            gauge1.setText( str(psi_readout_string), "Fuel Tank Pressure"     )
            gauge2.setText(str(psi_readout_string), "Fuel Flow Rate"         )
            gauge3.setText(str(psi_readout_string), "Fuel Injection Pressure")
            gauge4.setText(str(psi_readout_string), "Thrust"                 )
            gauge5.setText(str(psi_readout_string), "LOX Pressure"           )
            gauge6.setText(str(psi_readout_string), "LOX Flow Rate"          )
            gauge7.setText(str(psi_readout_string), "Engine Pressure"        )
            gauge8.setText(str(psi_readout_string), "LOX Temperature"        )

            gauge1.setAngle( psi_readout )
            gauge2.setAngle( psi_readout )
            gauge3.setAngle( psi_readout )
            gauge4.setAngle( psi_readout )
            gauge5.setAngle( psi_readout )
            gauge6.setAngle( psi_readout )
            gauge7.setAngle( psi_readout )
            gauge8.setAngle( psi_readout )

		    # Update engine schematic
            plumbing.updatePipeStatus()

            # Draw to main window
            root.update()

            # Draw to plumbing window
            plumbing.getWindow().update()
        except:
            exitFlag = True
            pass

	# Clear the console to get rid of weird tk/tcl errors
    os.system('cls' if os.name == 'nt' else 'clear')

###############################################################
# END OF FILE                                                 #
###############################################################
