####################################################################################
#                                                                                  #
# main.py -- main interface program for SDR's liquid engine                        #
#                                                                                  #
# Author: Nitish Chennoju, Colton Acosta                                           #
# Date: 6/12/2022                                                                  #
# Sun Devil Rocketry Avionics                                                      #
#                                                                                  #
####################################################################################


####################################################################################
# Developers                                                                       #
####################################################################################
__author__  =  "Nitish Chennoju"
__credits__ = ["Colton Acosta"   ,
               "Katie Herrington",
               "Ian Chandra"      ]


####################################################################################
# Standard Imports                                                                 #
####################################################################################

# General
import time
import os
import sys
import datetime

# Serial (USB)
import serial
import serial.tools.list_ports
from serial    import SerialException

# Interface/GUI
import tkinter as tk
from tkinter   import ttk
from PIL       import Image, ImageTk


####################################################################################
# Project Modules                                                                  #
####################################################################################

# Setup path 
sys.path.insert(0, './plumbing')
sys.path.insert(0, './sdec')

# Imports
import solenoid
import gauge          as SDR_gauge
import valve          as SDR_valve
import engine_display as SDR_engine_display
import sequence       as SDR_sequence
import buttons        as SDR_buttons
import sensor         as SDR_sensor

# SDEC 
import sdec
import commands
import hw_commands



####################################################################################
# Callbacks                                                                        #
####################################################################################

# Close all GUI windows
def close_window_callback():
    global exitFlag
    root.destroy()
    plumbing.win.destroy()
    exitFlag = True


####################################################################################
# Main application entry point                                                     #
####################################################################################
if __name__ == '__main__':

    ################################################################################
	# Serial Port Setup                                                            #
    ################################################################################

    # Initialize Serial Port Object
    terminalSerObj = sdec.terminalData()

    # Look for possible connections
    avail_ports = serial.tools.list_ports.comports()
    for port_num, port in enumerate( avail_ports ):
        if ( 'CP2102' in port.description ):
            # Connect
            port_num = port.device
            connect_args  = [ '-p', port_num]
            commands.connect( connect_args, terminalSerObj )
    
    ################################################################################
	# Data logging setup                                                           #
    ################################################################################

    # Get Date
    run_date = datetime.date.today()
    run_date = run_date.strftime("%m-%d-%Y")

    # Create Output directory
    if ( not ( os.path.exists( "output" ) ) ):
        os.mkdir( "output" )
    output_dir = "output/" + run_date
    if ( not ( os.path.exists( output_dir ) ) ):
        os.mkdir( "output/" + run_date )

    # Determine output filename based on existing files
    base_output_filename = output_dir + "/engine_data"
    test_num             = 0
    output_filename      = base_output_filename + str( test_num ) + ".txt"
    while ( os.path.exists( output_filename ) ):
        test_num        += 1
        output_filename  = base_output_filename + str( test_num ) + ".txt"


    ################################################################################
	# Global variables                                                             #
    ################################################################################

	# Declarations
    global exitFlag             # Flag set when window closes        

    # Initializations
    exitFlag = False

    ################################################################################
	# Local variables                                                              #
    ################################################################################

    # Spacing constants within GUI
    pad     = 10 
    gridLen = 85


    ################################################################################
	# Window frames                                                                #
    ################################################################################

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

    # Valve button frame
    valve_button_frame    = tk.Frame( root, bg = 'black' )

    # Valve button row frames
    valve_button_col1     = tk.Frame( valve_button_frame, bg = 'black' ) 
    valve_button_col2     = tk.Frame( valve_button_frame, bg = 'black' ) 

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


    ################################################################################
	# Widget initializations                                                       #
    ################################################################################

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
                                     valve_button_col1,
                                     "LOX Pressure (1)",
                                     'top'             ,
                                     plumbing.one
                                     )

    solenoid2_buttons = SDR_valve.Buttons(
                                     valve_button_col1,
                                     "LOX Vent (2)"   , 
                                     'top'         ,
                                     plumbing.two
                                     )

    solenoid3_buttons = SDR_valve.Buttons(
                                     valve_button_col1,
                                     "LOX Purge (5)"  , 
                                     'top'         ,
                                     plumbing.five
                                     )

    ball_valve1_buttons = SDR_valve.Buttons(
                                    valve_button_col1,
                                    "LOX Main"       ,
                                    'top'            ,
                                    plumbing.s2
                                    )

    solenoid5_buttons = SDR_valve.Buttons(
                                     valve_button_col2,
                                     "Fuel Pressure (3)", 
                                     'top'                  ,
                                     plumbing.three
                                     )

    solenoid6_buttons = SDR_valve.Buttons(
                                     valve_button_col2,
                                     "Fuel Vent (4)", 
                                     'top'              ,
                                     plumbing.four
                                     )

    solenoid4_buttons = SDR_valve.Buttons(
                                     valve_button_col2   ,
                                     "Fuel Purge (6)", 
                                     'top'               ,
                                     plumbing.six
                                     )


    ball_valve2_buttons = SDR_valve.Buttons(
                                    valve_button_col2    ,
                                    "Fuel Main Valve",
                                     'top'               ,
                                    plumbing.s1
                                    )

	# Startup button
    startup_button = SDR_buttons.Button(
                                        sequence_frame_row1      ,
                                        text          = "STARTUP",
                                        bg_color      = 'black'  ,
                                        fg_color      = 'white'  ,
                                        outline_color = 'white'  ,
                                        text_color    = 'white'  ,
                                        f_callback = SDR_sequence.startup
                                       )

	# All valves off button
    off_button   =   SDR_buttons.Button( 
                                        sequence_frame_row1      , 
                                        text          = "ABORT"  ,
                                        bg_color      = 'black'  ,
                                        fg_color      = 'white'  ,
                                        outline_color = 'white'  ,
                                        text_color    = 'white'  ,
                                        f_callback = SDR_sequence.allOff
                                       )

	# Sensor gauges
    gauge1 =      SDR_gauge.gauge( # Fuel Tank Pressure
                                 gauge_frame_row1    , 
                                 background = 'black',
                                 max_sensor_val = SDR_sensor.max_sensor_vals["pt0"]
                                 )

    gauge2 =      SDR_gauge.gauge( # Fuel Flow Rate
                                 gauge_frame_row1, 
                                 background = 'black',
                                 max_sensor_val = SDR_sensor.max_sensor_vals["pt1"]
                                 )

    gauge3 =      SDR_gauge.gauge( # Fuel Injection Pressure
                                 gauge_frame_row1, 
                                 background = 'black',
                                 max_sensor_val = SDR_sensor.max_sensor_vals["pt2"]
                                 )

    gauge4 =      SDR_gauge.gauge( # Thrust
                                 gauge_frame_row1, 
                                 background = 'black', 
                                 max_sensor_val = SDR_sensor.max_sensor_vals["lc"]
                                 )

    gauge5 =      SDR_gauge.gauge( # LOX Pressure
                                 gauge_frame_row2, 
                                 background = 'black', 
                                 max_sensor_val = SDR_sensor.max_sensor_vals["pt4"]
                                 )

    gauge6 =      SDR_gauge.gauge( # LOX Flow Rate
                                 gauge_frame_row2, 
                                 background = 'black', 
                                 max_sensor_val = SDR_sensor.max_sensor_vals["pt5"]
                                 )

    gauge7 =      SDR_gauge.gauge( # Engine Pressure
                                 gauge_frame_row2, 
                                 background = 'black', 
                                 max_sensor_val = SDR_sensor.max_sensor_vals["pt6"]
                                 )

    gauge8 =      SDR_gauge.gauge( # LOX Temperature
                                 gauge_frame_row2, 
                                 background = 'black', 
                                 max_sensor_val = SDR_sensor.max_sensor_vals["tc"]
                                 )

    gauge1.setText("Nan", "Fuel Tank Pressure"     )
    gauge2.setText("Nan", "Fuel Flow Rate"         )
    gauge3.setText("Nan", "Fuel Injection Pressure")
    gauge4.setText("Nan", "Thrust"                 )
    gauge5.setText("Nan", "LOX Pressure"           )
    gauge6.setText("Nan", "LOX Flow Rate"          )
    gauge7.setText("Nan", "Engine Pressure"        )
    gauge8.setText("Nan", "LOX Temperature"        )


    ################################################################################
	# Draw initial window                                                          #
    ################################################################################

	# Main window title
    main_title_frame.pack()
    SDRlabel.pack(side='left', padx=30)
    main_window_title.pack(pady=30, side='right')

	# Valve buttons
    valve_button_col1.pack( side = 'left'  )
    valve_button_col2.pack( side = 'right' )
    valve_button_frame.pack()

	# Sequence button frames
    sequence_frame_row1.pack()

	# Sequence frames
    startup_button.pack( side = "left"  )
    off_button.pack    ( side = "right" )

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


    ################################################################################
	# Main Program Loop                                                            #
    ################################################################################
    prevCon = True

    # Start timer
    start_time = time.perf_counter()

    # Update GUI
    while (not exitFlag):
        try:
            # Look for new serial connections 
            if ( terminalSerObj.comport == None ):
                avail_ports = serial.tools.list_ports.comports()
                for port_num, port in enumerate( avail_ports ):
                    if ( ( 'CP2102' in port.description ) or 
                         ( 'CP210x' in port.description ) ):
                        # Connect
                        port_num = port.device
                        connect_args  = [ '-p', port_num]
                        commands.connect( connect_args, terminalSerObj )

            else:
                # Record time of data reception
                time_sec = time.perf_counter() - start_time

                # Get sensor data
                sensor_args = ['dump']
                hw_commands.sensor( sensor_args, terminalSerObj )
                sensor_readouts_formatted = []
                for sensor in terminalSerObj.sensor_readouts:
                    sensor_readouts_formatted.append( SDR_sensor.format_sensor_readout(
                        terminalSerObj.controller,
                        sensor                   ,
                        terminalSerObj.sensor_readouts[sensor]
                    ) )

                # Update sensor gauge readings
                gauge1.setText( sensor_readouts_formatted[0], "Fuel Tank Pressure"     )
                gauge2.setText( sensor_readouts_formatted[1], "Fuel Flow Rate"         )
                gauge3.setText( sensor_readouts_formatted[2], "Fuel Injection Pressure")
                gauge4.setText( sensor_readouts_formatted[8], "Thrust"                 )
                gauge5.setText( sensor_readouts_formatted[3], "LOX Pressure"           )
                gauge6.setText( sensor_readouts_formatted[4], "LOX Flow Rate"          )
                gauge7.setText( sensor_readouts_formatted[5], "Engine Pressure"        )
                gauge8.setText( sensor_readouts_formatted[9], "LOX Temperature"        )

                gauge1.setAngle( terminalSerObj.sensor_readouts["pt0"] )
                gauge2.setAngle( terminalSerObj.sensor_readouts["pt1"] )
                gauge3.setAngle( terminalSerObj.sensor_readouts["pt2"] )
                gauge4.setAngle( terminalSerObj.sensor_readouts["lc"]  )
                gauge5.setAngle( terminalSerObj.sensor_readouts["pt3"] )
                gauge6.setAngle( terminalSerObj.sensor_readouts["pt4"] )
                gauge7.setAngle( terminalSerObj.sensor_readouts["pt5"] )
                gauge8.setAngle( terminalSerObj.sensor_readouts["tc"]  )

                # Log Data
                with open( output_filename, "a" ) as file:
                    file.write(str(time_sec) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["pt0"]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["pt1"]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["pt2"]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["pt3"]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["pt4"]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["pt5"]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["pt6"]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["pt7"]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["lc"] ) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["tc"] ) + " ")
                    file.write("\n")

            # Update engine schematic
            plumbing.updatePipeStatus()

            # Draw to main window
            root.update()

            # Draw to plumbing window
            plumbing.getWindow().update()

        # Exit App
        except:
            exitFlag = True
            pass

	# Clear the console to get rid of weird tk/tcl errors
    os.system('cls' if os.name == 'nt' else 'clear')


####################################################################################
# END OF FILE                                                                      #
####################################################################################