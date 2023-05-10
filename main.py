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
import math

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
import sensor_conv
import engineController


####################################################################################
# Defines                                                                          #
####################################################################################

# Valve open/close states
VALVE_OPEN   = True
VALVE_CLOSED = False

# Filter enable for gauge readouts
GAUGE_FILTER_ENABLED = True


####################################################################################
# Objects                                                                          #
####################################################################################


####################################################################################
#                                                                                  #
# OBJECT:                                                                          #
# 		liquid_engine_state                                                        #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Contains state information on the liquid engine                            #
#                                                                                  #
####################################################################################
class Liquid_Engine_State:

    # Initialzation Function
    def __init__( self ):
        self.state = "Initialization State"
    ## __init__ ##

    # Get the engine state
    def get_engine_state( self ):
        return self.state
    ## get_engine_state ##

    # Set the engine state
    def set_engine_state( self, new_engine_state ):
        self.state = new_engine_state
    ## set_engine_state ## 
## liquid_engine_state ##


####################################################################################
#                                                                                  #
# OBJECT:                                                                          #
# 		Sensor_Data_Buffer                                                         #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Contains a queue of previous sensor data for filtering of gauge readouts   #
#                                                                                  #
####################################################################################
class Sensor_Data_Buffer:

    # Initialization
    # max_buffer_size: size of the FIFO buffer
    # tau            : time constant of low-pass filter
    def __init__( self, max_buffer_size = 10, tau = 1 ):
        self.data_buffer     = []
        self.filter_buffer   = []
        self.buffer_size     = 0
        self.max_buffer_size = max_buffer_size
        self.tau             = tau
        self.sensors         = [ "pt0", "pt1", "pt2", "pt3", "pt4", "pt5", "pt6", 
                                 "pt7", "lc", "tc"]
    ## __init__ ##

    # Add data to the buffer 
    def add_data( self, sensor_data ):
        if ( self.buffer_size < self.max_buffer_size ):
            self.data_buffer.append( sensor_data )
            self.buffer_size += 1
            if ( self.buffer_size == 1 ):
                self.filter_buffer.append( sensor_data )
            else:
                self.filter_buffer.append( self.filter_data() ) 
        else:
            self.data_buffer.pop( 0 )
            self.data_buffer.append( sensor_data )
            self.filter_buffer.append( self.filter_data() )
    ## add_data ##

    # Filter incoming data 
    def filter_data( self ):
        # Calculate filter coefficients
        T     = self.data_buffer[-1]["t"] - self.data_buffer[-2]["t"] # Time period
        alpha = 2*self.tau + T
        beta  = T - 2*self.tau

        # Difference equation
        filtered_readouts = {}
        for sensor in self.sensors:
            filtered_readouts[sensor] = ( (T/alpha)*( self.data_buffer[-1][sensor] +
            self.data_buffer[-2][sensor] ) - (beta/alpha)*(self.filter_buffer[-1][sensor]) )
        return filtered_readouts
    ## filter_data ##

    ## Get the most recent filter data
    def get_data( self ):
        return self.filter_buffer[-1]
## Sensor_Data_Buffer ##


####################################################################################
# Callbacks                                                                        #
####################################################################################

# Close all GUI windows
def close_window_callback():
    global exitFlag
    root.destroy()
    plumbing.win.destroy()
    exitFlag = True

# Sequencing/Control callbacks
def pre_fire_purge_callback():
    SDR_sequence.pre_fire_purge( liquid_engine_state, terminalSerObj )

def fill_and_chill_callback():
    SDR_sequence.fill_and_chill( liquid_engine_state, terminalSerObj )

def standby_callback():
    SDR_sequence.standby       ( liquid_engine_state, terminalSerObj )

def fire_engine_callback():
    SDR_sequence.fire_engine   ( liquid_engine_state, terminalSerObj )

def hotfire_abort_callback():
    SDR_sequence.hotfire_abort ( liquid_engine_state, terminalSerObj )

def get_state_callback():
    SDR_sequence.get_state     ( liquid_engine_state, terminalSerObj )

def stop_hotfire_callback():
    SDR_sequence.stop_hotfire  ( liquid_engine_state, terminalSerObj )

def stop_purge_callback():
    SDR_sequence.stop_purge    ( liquid_engine_state, terminalSerObj )

def lox_purge_callback():
    SDR_sequence.lox_purge     ( liquid_engine_state, terminalSerObj )

def kbottle_close_callback():
    SDR_sequence.kbottle_close ( liquid_engine_state, terminalSerObj )

def manual_mode_callback():
    SDR_sequence.manual        ( liquid_engine_state, terminalSerObj )

def lox_press_callback():
    SDR_sequence.manual_lox_press ( liquid_engine_state, terminalSerObj, solenoid1_buttons.state )
    if ( ( solenoid1_buttons.symbol != None ) and ( liquid_engine_state.state == "Manual State" ) ):
        solenoid1_buttons.state = not solenoid1_buttons.state 
        solenoid1_buttons.symbol.setState( solenoid1_buttons.state )
        solenoid1_buttons.updateText()
        solenoid1_buttons.updateColor()
        solenoid1_buttons.configButton()

def lox_vent_callback():
    SDR_sequence.manual_lox_vent ( liquid_engine_state, terminalSerObj, solenoid2_buttons.state )
    if ( ( solenoid2_buttons.symbol != None ) and ( liquid_engine_state.state == "Manual State" ) ):
        solenoid2_buttons.state = not solenoid2_buttons.state 
        solenoid2_buttons.symbol.setState( solenoid2_buttons.state )
        solenoid2_buttons.updateText()
        solenoid2_buttons.updateColor()
        solenoid2_buttons.configButton()

def manual_lox_purge_callback():
    SDR_sequence.manual_lox_purge( liquid_engine_state, terminalSerObj, solenoid3_buttons.state )
    if ( ( solenoid3_buttons.symbol != None ) and ( liquid_engine_state.state == "Manual State" ) ):
        solenoid3_buttons.state = not solenoid3_buttons.state 
        solenoid3_buttons.symbol.setState( solenoid3_buttons.state )
        solenoid3_buttons.updateText()
        solenoid3_buttons.updateColor()
        solenoid3_buttons.configButton()

def fuel_purge_callback():
    SDR_sequence.manual_fuel_purge( liquid_engine_state, terminalSerObj, solenoid4_buttons.state )
    if ( ( solenoid4_buttons.symbol != None ) and ( liquid_engine_state.state == "Manual State" ) ):
        solenoid4_buttons.state = not solenoid4_buttons.state 
        solenoid4_buttons.symbol.setState( solenoid4_buttons.state )
        solenoid4_buttons.updateText()
        solenoid4_buttons.updateColor()
        solenoid4_buttons.configButton()

def fuel_press_callback():
    SDR_sequence.manual_fuel_press( liquid_engine_state, terminalSerObj, solenoid5_buttons.state )
    if ( ( solenoid5_buttons.symbol != None ) and ( liquid_engine_state.state == "Manual State" ) ):
        solenoid5_buttons.state = not solenoid5_buttons.state 
        solenoid5_buttons.symbol.setState( solenoid5_buttons.state )
        solenoid5_buttons.updateText()
        solenoid5_buttons.updateColor()
        solenoid5_buttons.configButton()

def fuel_vent_callback():
    SDR_sequence.manual_fuel_vent( liquid_engine_state, terminalSerObj, solenoid6_buttons.state )
    if ( ( solenoid6_buttons.symbol != None ) and ( liquid_engine_state.state == "Manual State" ) ):
        solenoid6_buttons.state = not solenoid6_buttons.state 
        solenoid6_buttons.symbol.setState( solenoid6_buttons.state )
        solenoid6_buttons.updateText()
        solenoid6_buttons.updateColor()
        solenoid6_buttons.configButton()

def lox_main_callback():
    SDR_sequence.manual_lox_main( liquid_engine_state, terminalSerObj, ball_valve1_buttons.state )
    if ( ( ball_valve1_buttons.symbol != None ) and ( liquid_engine_state.state == "Manual State" ) ):
        ball_valve1_buttons.state = not ball_valve1_buttons.state 
        ball_valve1_buttons.symbol.setState( ball_valve1_buttons.state )
        ball_valve1_buttons.updateText()
        ball_valve1_buttons.updateColor()
        ball_valve1_buttons.configButton()

def fuel_main_callback():
    SDR_sequence.manual_fuel_main( liquid_engine_state, terminalSerObj, ball_valve2_buttons.state )
    if ( ( ball_valve2_buttons.symbol != None ) and ( liquid_engine_state.state == "Manual State" ) ):
        ball_valve2_buttons.state = not ball_valve2_buttons.state 
        ball_valve2_buttons.symbol.setState( ball_valve2_buttons.state )
        ball_valve2_buttons.updateText()
        ball_valve2_buttons.updateColor()
        ball_valve2_buttons.configButton()


####################################################################################
# Procedures #
####################################################################################

# Update the valves state after telreq
def update_valve_states( valve_states ):
    # LOX Pressure
    if ( valve_states["oxPress"] == "OPEN" ):
        solenoid1_buttons.symbol.setState( VALVE_OPEN )
        solenoid1_buttons.state = VALVE_OPEN
    elif ( valve_states["oxPress"] == "CLOSED" ):
        solenoid1_buttons.symbol.setState( VALVE_CLOSED )
        solenoid1_buttons.state = VALVE_CLOSED
    solenoid1_buttons.updateText()
    solenoid1_buttons.updateColor()
    solenoid1_buttons.configButton()

    # LOX Vent
    if ( valve_states["oxVent"] == "OPEN" ):
        solenoid2_buttons.symbol.setState( VALVE_OPEN )
    elif ( valve_states["oxVent"] == "CLOSED" ):
        solenoid2_buttons.symbol.setState( VALVE_CLOSED )
    solenoid2_buttons.updateText()
    solenoid2_buttons.updateColor()
    solenoid2_buttons.configButton()
    
    # LOX Purge
    if ( valve_states["oxPurge"] == "OPEN" ):
        solenoid3_buttons.symbol.setState( VALVE_OPEN )
    elif ( valve_states["oxPurge"] == "CLOSED" ):
        solenoid3_buttons.symbol.setState( VALVE_CLOSED )
    solenoid3_buttons.updateText()
    solenoid3_buttons.updateColor()
    solenoid3_buttons.configButton()

    # Fuel Purge
    if ( valve_states["fuelPurge"] == "OPEN" ):
        solenoid4_buttons.symbol.setState( VALVE_OPEN )
    elif ( valve_states["fuelPurge"] == "CLOSED" ):
        solenoid4_buttons.symbol.setState( VALVE_CLOSED )
    solenoid4_buttons.updateText()
    solenoid4_buttons.updateColor()
    solenoid4_buttons.configButton()

    # Fuel Pressure
    if ( valve_states["fuelPress"] == "OPEN" ):
        solenoid5_buttons.symbol.setState( VALVE_OPEN )
    elif ( valve_states["fuelPress"] == "CLOSED" ):
        solenoid5_buttons.symbol.setState( VALVE_CLOSED )
    solenoid5_buttons.updateText()
    solenoid5_buttons.updateColor()
    solenoid5_buttons.configButton()

    # Fuel Vent
    if ( valve_states["fuelVent"] == "OPEN" ):
        solenoid6_buttons.symbol.setState( VALVE_OPEN )
    elif ( valve_states["fuelVent"] == "CLOSED" ):
        solenoid6_buttons.symbol.setState( VALVE_CLOSED )
    solenoid6_buttons.updateText()
    solenoid6_buttons.updateColor()
    solenoid6_buttons.configButton()

    # LOX Main
    if ( valve_states["oxMain"] == "OPEN" ):
        ball_valve1_buttons.symbol.setState( VALVE_OPEN )
    elif ( valve_states["oxMain"] == "CLOSED" ):
        ball_valve1_buttons.symbol.setState( VALVE_CLOSED )
    ball_valve1_buttons.updateText()
    ball_valve1_buttons.updateColor()
    ball_valve1_buttons.configButton()

    # Fuel Main
    if ( valve_states["fuelMain"] == "OPEN" ):
        ball_valve2_buttons.symbol.setState( VALVE_OPEN )
    elif ( valve_states["fuelMain"] == "CLOSED" ):
        ball_valve2_buttons.symbol.setState( VALVE_CLOSED )
    ball_valve2_buttons.updateText()
    ball_valve2_buttons.updateColor()
    ball_valve2_buttons.configButton()
## update_valve_states ##


####################################################################################
# Global Variables                                                                 #
####################################################################################

# State of the engine
liquid_engine_state = Liquid_Engine_State()

# Buffer for filtering data prior to displaying on gauges
sensor_data_buffer = Sensor_Data_Buffer( tau = 10 )

# File Name outputs
engine_state_filenames = {
                        "Initialization State": "init"    ,
                        "Ready State"         : "ready"   ,
                        "Pre-Fire Purge State": "pfpurge" ,
                        "Fill and Chill State": "fillchill",
                        "Standby State"       : "standby" ,
                        "Fire State"          : "fire"    ,
                        "Disarm State"        : "disarm"  ,
                        "Post-Fire State"     : "postfire",
                        "Manual State"        : "manual"  ,
                        "Abort"               : "abort"
                         }


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

            # Enter the ready state
            liquid_engine_state.set_engine_state( "Ready State" )
    
    ################################################################################
	# Data logging setup                                                           #
    ################################################################################

    # Get Date
    run_date = datetime.date.today()
    run_date = run_date.strftime("%m-%d-%Y")

    # Create Output directory
    if ( not ( os.path.exists( "output" ) ) ):
        os.mkdir( "output" )
    output_dir = "output/" + "hotfire/"
    if ( not ( os.path.exists( output_dir ) ) ):
        os.mkdir( output_dir )
    output_dir += run_date
    if ( not ( os.path.exists( output_dir ) ) ):
        os.mkdir( output_dir )

    # Determine output filename based on existing files
    base_output_filename = output_dir + "/" + engine_state_filenames[liquid_engine_state.state]
    test_num             = 0
    output_filename      = base_output_filename + str( test_num ) + ".txt"
    while ( os.path.exists( output_filename ) ):
        test_num        += 1
        output_filename  = base_output_filename + str( test_num ) + ".txt"

    # Create an initial File
    with open( output_filename, "a" ) as file:
        file.write( "Initialization State" ) 


    ################################################################################
	# Global variables                                                             #
    ################################################################################

	# Declarations
    global exitFlag             # Flag set when window closes        

    # Initializations
    exitFlag = False

    # Timing
    safe_tanks_timing_cnt = 1

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
    #root.iconphoto(True, SDRlogo)

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
    valve_button_col3     = tk.Frame( valve_button_frame, bg = 'black' )

	# Sequence button frames
    sequence_frame_row1 = tk.Frame(
                                  root,
								  bg='black'
                                  )
    sequence_frame_row2 = tk.Frame(
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
                                     plumbing.one, 
                                     f_callback = lox_press_callback
                                     )

    solenoid2_buttons = SDR_valve.Buttons(
                                     valve_button_col1,
                                     "LOX Vent (2)"   , 
                                     'top'         ,
                                     plumbing.two,
                                     f_callback = lox_vent_callback
                                     )

    solenoid3_buttons = SDR_valve.Buttons(
                                     valve_button_col1,
                                     "LOX Purge (5)"  , 
                                     'top'         ,
                                     plumbing.five,
                                     f_callback = manual_lox_purge_callback
                                     )

    ball_valve1_buttons = SDR_valve.Buttons(
                                    valve_button_col1,
                                    "LOX Main"       ,
                                    'top'            ,
                                    plumbing.s2,
                                    f_callback = lox_main_callback
                                    )

    solenoid5_buttons = SDR_valve.Buttons(
                                     valve_button_col2,
                                     "Fuel Pressure (3)", 
                                     'top'                  ,
                                     plumbing.three,
                                     f_callback = fuel_press_callback
                                     )

    solenoid6_buttons = SDR_valve.Buttons(
                                     valve_button_col2,
                                     "Fuel Vent (4)", 
                                     'top'              ,
                                     plumbing.four,
                                     f_callback = fuel_vent_callback
                                     )

    solenoid4_buttons = SDR_valve.Buttons(
                                     valve_button_col2   ,
                                     "Fuel Purge (6)", 
                                     'top'               ,
                                     plumbing.six,
                                     f_callback = fuel_purge_callback
                                     )


    ball_valve2_buttons = SDR_valve.Buttons(
                                    valve_button_col2    ,
                                    "Fuel Main Valve",
                                     'top'               ,
                                    plumbing.s1,
                                    f_callback = fuel_main_callback
                                    )

	# Pre-Fire purge button
    pre_fire_purge_button = SDR_buttons.Button(
                            sequence_frame_row1      ,
                            text          = "Pre-Fire Purge",
                            bg_color      = 'black'  ,
                            fg_color      = 'white'  ,
                            outline_color = 'white'  ,
                            text_color    = 'white'  ,
                            size          = ( 135, 45 ),
                            f_callback = pre_fire_purge_callback
                                              )
    
    # Fill and chill button
    fill_chill_button =     SDR_buttons.Button(
                            sequence_frame_row1         ,
                            text          = "Fill/Chill",
                            bg_color      = 'black'     ,
                            fg_color      = 'white'     ,
                            outline_color = 'white'     ,
                            text_color    = 'white'     ,
                            size          = ( 135, 45 ) ,
                            f_callback    = fill_and_chill_callback
                                              )
    
    # Standby button
    standby_button =        SDR_buttons.Button(
                            sequence_frame_row1         ,
                            text          = "Standby",
                            bg_color      = 'black'     ,
                            fg_color      = 'white'     ,
                            outline_color = 'white'     ,
                            text_color    = 'white'     ,
                            size          = ( 135, 45 ) ,
                            f_callback    = standby_callback 
                                              )

    # Standby button
    ignite_button =         SDR_buttons.Button(
                            sequence_frame_row1         ,
                            text          = "Ignite"    ,
                            bg_color      = 'black'     ,
                            fg_color      = 'white'     ,
                            outline_color = 'white'     ,
                            text_color    = 'white'     ,
                            size          = ( 135, 45 ) ,
                            f_callback    = fire_engine_callback 
                                              )

    # Stop hotfire button
    stop_hotfire_button =   SDR_buttons.Button( 
                            sequence_frame_row2      , 
                            text          = "Stop Hotfire" ,
                            bg_color      = 'black'  ,
                            fg_color      = 'white'  ,
                            outline_color = 'white'  ,
                            text_color    = 'white'  ,
                            size          = ( 135, 45 ),
                            f_callback = stop_hotfire_callback 
                                              )
    # Stop purge button
    stop_purge_button =     SDR_buttons.Button( 
                            sequence_frame_row2      , 
                            text          = "Disarm" ,
                            bg_color      = 'black'  ,
                            fg_color      = 'white'  ,
                            outline_color = 'white'  ,
                            text_color    = 'white'  ,
                            size          = ( 135, 45 ),
                            f_callback = stop_purge_callback
                                              )
    # LOX purge button
    lox_purge_button =      SDR_buttons.Button( 
                            sequence_frame_row2      , 
                            text          = "LOX Purge" ,
                            bg_color      = 'black'  ,
                            fg_color      = 'white'  ,
                            outline_color = 'white'  ,
                            text_color    = 'white'  ,
                            size          = ( 135, 45 ),
                            f_callback = lox_purge_callback 
                                              )
    
    # Kbottle close button
    kbottle_close_button =  SDR_buttons.Button( 
                            sequence_frame_row2      , 
                            text          = "KBottle Close" ,
                            bg_color      = 'black'  ,
                            fg_color      = 'white'  ,
                            outline_color = 'white'  ,
                            text_color    = 'white'  ,
                            size          = ( 135, 45 ),
                            f_callback = kbottle_close_callback 
                                              )

	# Get state button 
    getstate_button =       SDR_buttons.Button( 
                            valve_button_col3          , 
                            text          = "Get State",
                            bg_color      = 'black'    ,
                            fg_color      = 'white'    ,
                            outline_color = 'white'    ,
                            text_color    = 'white'    ,
                            size          = ( 135, 45 ),
                            f_callback = get_state_callback
                                              )

	# Abort button
    abort_button =          SDR_buttons.Button( 
                            valve_button_col3        , 
                            text          = "ABORT"  ,
                            bg_color      = 'black'  ,
                            fg_color      = 'red'    ,
                            outline_color = 'red'    ,
                            text_color    = 'red'    ,
                            size          = ( 135, 45 ),
                            f_callback = hotfire_abort_callback 
                                              )

	# Abort button
    manual_mode_button =    SDR_buttons.Button( 
                            valve_button_col3        , 
                            text          = "Manual"  ,
                            bg_color      = 'black'  ,
                            fg_color      = 'white'    ,
                            outline_color = 'white'    ,
                            text_color    = 'white'    ,
                            size          = ( 135, 45 ),
                            f_callback = manual_mode_callback 
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
                                 max_sensor_val = SDR_sensor.max_sensor_vals["ffr"]
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
                                 max_sensor_val = SDR_sensor.max_sensor_vals["oxfr"]
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
    gauge3.setText("Nan", "None"                   )
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
    valve_button_col1.pack( side = 'left' )
    valve_button_col2.pack( side = 'left' )
    valve_button_col3.pack( side = 'left' )
    valve_button_frame.pack()

	# Sequence button frames
    sequence_frame_row1.pack()
    sequence_frame_row2.pack()

	# Sequence frames
    pre_fire_purge_button.pack( side = "left", padx = 30 )
    fill_chill_button.pack    ( side = "left", padx = 30 )
    standby_button.pack       ( side = "left", padx = 30 )
    ignite_button.pack        ( side = "left", padx = 30 )
    getstate_button.pack      ( side = "top" , padx = 30 )
    manual_mode_button.pack   ( side = "top" , padx = 30 )
    abort_button.pack         ( side = "top" , padx = 30 )
    stop_hotfire_button.pack  ( side = "left", padx = 30 )
    stop_purge_button.pack    ( side = "left", padx = 30 )
    lox_purge_button.pack     ( side = "left", padx = 30 )
    kbottle_close_button.pack ( side = "left", padx = 30 )

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

                    # Transition into the ready state
                    liquid_engine_state.set_engine_state( "Ready State" )


        # Connection is made
        else:
            # Record time of data reception
            time_sec = time.perf_counter() - start_time

            ####################################################################
            # Ready State                                                      #
            ####################################################################
            if ( liquid_engine_state.get_engine_state() == "Ready State" ):
                # Get telemetry
                engineController.telreq( [], terminalSerObj, show_output = False )
                terminalSerObj.sensor_readouts["t"] = time_sec
                sensor_readouts_formatted = {}
                for sensor in terminalSerObj.sensor_readouts:
                    sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                        terminalSerObj.controller,
                        sensor                   ,
                        terminalSerObj.sensor_readouts[sensor] ) 

                # Filter the data
                if ( GAUGE_FILTER_ENABLED ):
                    sensor_data_buffer.add_data( terminalSerObj.sensor_readouts )
                    sensor_data_filtered = sensor_data_buffer.get_data()
                    filtered_sensor_readouts_formatted = {}
                    for sensor in sensor_data_filtered:
                        filtered_sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                            terminalSerObj.controller,
                            sensor                   ,
                            sensor_data_filtered[sensor] ) 

                # Calculate Flow Rates
                if ( GAUGE_FILTER_ENABLED ):
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                sensor_data_filtered["pt1"] -
                                                sensor_data_filtered["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                sensor_data_filtered["pt6"] -
                                                sensor_data_filtered["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )
                else:
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                terminalSerObj.sensor_readouts["pt1"] -
                                                terminalSerObj.sensor_readouts["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                terminalSerObj.sensor_readouts["pt6"] -
                                                terminalSerObj.sensor_readouts["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )

                # Update GUI
                if ( GAUGE_FILTER_ENABLED ):
                    gauge1.setText( filtered_sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( filtered_sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( filtered_sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( filtered_sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( filtered_sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( sensor_data_filtered["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( sensor_data_filtered["lc" ] )
                    gauge5.setAngle( sensor_data_filtered["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( sensor_data_filtered["pt4"] )
                    gauge8.setAngle( sensor_data_filtered["tc" ] )
                else:
                    gauge1.setText( sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( terminalSerObj.sensor_readouts["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( terminalSerObj.sensor_readouts["lc" ] )
                    gauge5.setAngle( terminalSerObj.sensor_readouts["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( terminalSerObj.sensor_readouts["pt4"] )
                    gauge8.setAngle( terminalSerObj.sensor_readouts["tc" ] )
                update_valve_states( terminalSerObj.valve_states )


                # Log Data
                base_output_filename = output_dir + "/" + engine_state_filenames[liquid_engine_state.state]
                output_filename      = base_output_filename + str( test_num ) + ".txt"
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
                    file.write(str(terminalSerObj.sensor_readouts["lc" ]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["tc" ]) + " ")
                    file.write(terminalSerObj.valve_states["oxPress"  ]   + " ")
                    file.write(terminalSerObj.valve_states["oxVent"   ]   + " ")
                    file.write(terminalSerObj.valve_states["oxPurge"  ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPress"]   + " ")
                    file.write(terminalSerObj.valve_states["fuelVent" ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPurge"]   + " ")
                    file.write(terminalSerObj.valve_states["oxMain"   ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelMain" ]   + " ")
                    file.write("\n")

            ####################################################################
            # Pre-Fire Engine Purge                                            #
            ####################################################################
            elif ( liquid_engine_state.get_engine_state() == "Pre-Fire Purge State" ):
                # Get telemetry
                engineController.telreq( [], terminalSerObj, show_output = False )
                terminalSerObj.sensor_readouts["t"] = time_sec
                sensor_readouts_formatted = {}
                for sensor in terminalSerObj.sensor_readouts:
                    sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                        terminalSerObj.controller,
                        sensor                   ,
                        terminalSerObj.sensor_readouts[sensor] ) 

                # Filter the data
                if ( GAUGE_FILTER_ENABLED ):
                    sensor_data_buffer.add_data( terminalSerObj.sensor_readouts )
                    sensor_data_filtered = sensor_data_buffer.get_data()
                    filtered_sensor_readouts_formatted = {}
                    for sensor in sensor_data_filtered:
                        filtered_sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                            terminalSerObj.controller,
                            sensor                   ,
                            sensor_data_filtered[sensor] ) 

                # Calculate Flow Rates
                if ( GAUGE_FILTER_ENABLED ):
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                sensor_data_filtered["pt1"] -
                                                sensor_data_filtered["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                sensor_data_filtered["pt6"] -
                                                sensor_data_filtered["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )
                else:
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                terminalSerObj.sensor_readouts["pt1"] -
                                                terminalSerObj.sensor_readouts["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                terminalSerObj.sensor_readouts["pt6"] -
                                                terminalSerObj.sensor_readouts["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )

                # Update GUI
                if ( GAUGE_FILTER_ENABLED ):
                    gauge1.setText( filtered_sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( filtered_sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( filtered_sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( filtered_sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( filtered_sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( sensor_data_filtered["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( sensor_data_filtered["lc" ] )
                    gauge5.setAngle( sensor_data_filtered["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( sensor_data_filtered["pt4"] )
                    gauge8.setAngle( sensor_data_filtered["tc" ] )
                else:
                    gauge1.setText( sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( terminalSerObj.sensor_readouts["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( terminalSerObj.sensor_readouts["lc" ] )
                    gauge5.setAngle( terminalSerObj.sensor_readouts["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( terminalSerObj.sensor_readouts["pt4"] )
                    gauge8.setAngle( terminalSerObj.sensor_readouts["tc" ] )
                update_valve_states( terminalSerObj.valve_states )

                # Log Data
                base_output_filename = output_dir + "/" + engine_state_filenames[liquid_engine_state.state]
                output_filename      = base_output_filename + str( test_num ) + ".txt"
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
                    file.write(str(terminalSerObj.sensor_readouts["lc" ]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["tc" ]) + " ")
                    file.write(terminalSerObj.valve_states["oxPress"  ]   + " ")
                    file.write(terminalSerObj.valve_states["oxVent"   ]   + " ")
                    file.write(terminalSerObj.valve_states["oxPurge"  ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPress"]   + " ")
                    file.write(terminalSerObj.valve_states["fuelVent" ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPurge"]   + " ")
                    file.write(terminalSerObj.valve_states["oxMain"   ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelMain" ]   + " ")
                    file.write("\n")

            ####################################################################
            # Fill and Chill                                                   #
            ####################################################################
            elif ( liquid_engine_state.get_engine_state() == "Fill and Chill State"):
                # Check tank pressures
                engineController.tankstat( [], terminalSerObj )

                # Get telemetry
                engineController.telreq( [], terminalSerObj, show_output = False )
                terminalSerObj.sensor_readouts["t"] = time_sec
                sensor_readouts_formatted = {}
                for sensor in terminalSerObj.sensor_readouts:
                    sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                        terminalSerObj.controller,
                        sensor                   ,
                        terminalSerObj.sensor_readouts[sensor] ) 

                # Filter the data
                if ( GAUGE_FILTER_ENABLED ):
                    sensor_data_buffer.add_data( terminalSerObj.sensor_readouts )
                    sensor_data_filtered = sensor_data_buffer.get_data()
                    filtered_sensor_readouts_formatted = {}
                    for sensor in sensor_data_filtered:
                        filtered_sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                            terminalSerObj.controller,
                            sensor                   ,
                            sensor_data_filtered[sensor] ) 

                # Calculate Flow Rates
                if ( GAUGE_FILTER_ENABLED ):
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                sensor_data_filtered["pt1"] -
                                                sensor_data_filtered["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                sensor_data_filtered["pt6"] -
                                                sensor_data_filtered["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )
                else:
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                terminalSerObj.sensor_readouts["pt1"] -
                                                terminalSerObj.sensor_readouts["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                terminalSerObj.sensor_readouts["pt6"] -
                                                terminalSerObj.sensor_readouts["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )

                # Update GUI
                if ( GAUGE_FILTER_ENABLED ):
                    gauge1.setText( filtered_sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( filtered_sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( filtered_sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( filtered_sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( filtered_sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( sensor_data_filtered["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( sensor_data_filtered["lc" ] )
                    gauge5.setAngle( sensor_data_filtered["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( sensor_data_filtered["pt4"] )
                    gauge8.setAngle( sensor_data_filtered["tc" ] )
                else:
                    gauge1.setText( sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( terminalSerObj.sensor_readouts["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( terminalSerObj.sensor_readouts["lc" ] )
                    gauge5.setAngle( terminalSerObj.sensor_readouts["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( terminalSerObj.sensor_readouts["pt4"] )
                    gauge8.setAngle( terminalSerObj.sensor_readouts["tc" ] )
                update_valve_states( terminalSerObj.valve_states )

                # Log Data
                base_output_filename = output_dir + "/" + engine_state_filenames[liquid_engine_state.state]
                output_filename      = base_output_filename + str( test_num ) + ".txt"
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
                    file.write(str(terminalSerObj.sensor_readouts["lc" ]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["tc" ]) + " ")
                    file.write(terminalSerObj.valve_states["oxPress"  ]   + " ")
                    file.write(terminalSerObj.valve_states["oxVent"   ]   + " ")
                    file.write(terminalSerObj.valve_states["oxPurge"  ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPress"]   + " ")
                    file.write(terminalSerObj.valve_states["fuelVent" ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPurge"]   + " ")
                    file.write(terminalSerObj.valve_states["oxMain"   ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelMain" ]   + " ")
                    file.write("\n")

            ####################################################################
            # Standby                                                          #
            ####################################################################
            elif ( liquid_engine_state.get_engine_state() == "Standby State"):
                # Get telemetry
                engineController.telreq( [], terminalSerObj, show_output = False )
                terminalSerObj.sensor_readouts["t"] = time_sec
                sensor_readouts_formatted = {}
                for sensor in terminalSerObj.sensor_readouts:
                    sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                        terminalSerObj.controller,
                        sensor                   ,
                        terminalSerObj.sensor_readouts[sensor] ) 

                # Filter the data
                if ( GAUGE_FILTER_ENABLED ):
                    sensor_data_buffer.add_data( terminalSerObj.sensor_readouts )
                    sensor_data_filtered = sensor_data_buffer.get_data()
                    filtered_sensor_readouts_formatted = {}
                    for sensor in sensor_data_filtered:
                        filtered_sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                            terminalSerObj.controller,
                            sensor                   ,
                            sensor_data_filtered[sensor] ) 

                # Calculate Flow Rates
                if ( GAUGE_FILTER_ENABLED ):
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                sensor_data_filtered["pt1"] -
                                                sensor_data_filtered["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                sensor_data_filtered["pt6"] -
                                                sensor_data_filtered["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )
                else:
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                terminalSerObj.sensor_readouts["pt1"] -
                                                terminalSerObj.sensor_readouts["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                terminalSerObj.sensor_readouts["pt6"] -
                                                terminalSerObj.sensor_readouts["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )

                # Update GUI
                if ( GAUGE_FILTER_ENABLED ):
                    gauge1.setText( filtered_sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( filtered_sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( filtered_sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( filtered_sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( filtered_sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( sensor_data_filtered["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( sensor_data_filtered["lc" ] )
                    gauge5.setAngle( sensor_data_filtered["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( sensor_data_filtered["pt4"] )
                    gauge8.setAngle( sensor_data_filtered["tc" ] )
                else:
                    gauge1.setText( sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( terminalSerObj.sensor_readouts["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( terminalSerObj.sensor_readouts["lc" ] )
                    gauge5.setAngle( terminalSerObj.sensor_readouts["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( terminalSerObj.sensor_readouts["pt4"] )
                    gauge8.setAngle( terminalSerObj.sensor_readouts["tc" ] )
                update_valve_states( terminalSerObj.valve_states )

                # Log Data
                base_output_filename = output_dir + "/" + engine_state_filenames[liquid_engine_state.state]
                output_filename      = base_output_filename + str( test_num ) + ".txt"
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
                    file.write(str(terminalSerObj.sensor_readouts["lc" ]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["tc" ]) + " ")
                    file.write(terminalSerObj.valve_states["oxPress"  ]   + " ")
                    file.write(terminalSerObj.valve_states["oxVent"   ]   + " ")
                    file.write(terminalSerObj.valve_states["oxPurge"  ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPress"]   + " ")
                    file.write(terminalSerObj.valve_states["fuelVent" ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPurge"]   + " ")
                    file.write(terminalSerObj.valve_states["oxMain"   ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelMain" ]   + " ")
                    file.write("\n")

            ####################################################################
            # Engine Hotfire                                                   #
            ####################################################################
            elif ( liquid_engine_state.get_engine_state() == "Fire State"):
                # Get telemetry
                engineController.telreq( [], terminalSerObj, show_output = False )
                terminalSerObj.sensor_readouts["t"] = time_sec
                sensor_readouts_formatted = {}
                for sensor in terminalSerObj.sensor_readouts:
                    sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                        terminalSerObj.controller,
                        sensor                   ,
                        terminalSerObj.sensor_readouts[sensor] ) 

                # Filter the data
                if ( GAUGE_FILTER_ENABLED ):
                    sensor_data_buffer.add_data( terminalSerObj.sensor_readouts )
                    sensor_data_filtered = sensor_data_buffer.get_data()
                    filtered_sensor_readouts_formatted = {}
                    for sensor in sensor_data_filtered:
                        filtered_sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                            terminalSerObj.controller,
                            sensor                   ,
                            sensor_data_filtered[sensor] ) 

                # Calculate Flow Rates
                if ( GAUGE_FILTER_ENABLED ):
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                sensor_data_filtered["pt1"] -
                                                sensor_data_filtered["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                sensor_data_filtered["pt6"] -
                                                sensor_data_filtered["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )
                else:
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                terminalSerObj.sensor_readouts["pt1"] -
                                                terminalSerObj.sensor_readouts["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                terminalSerObj.sensor_readouts["pt6"] -
                                                terminalSerObj.sensor_readouts["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )

                # Update GUI
                if ( GAUGE_FILTER_ENABLED ):
                    gauge1.setText( filtered_sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( filtered_sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( filtered_sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( filtered_sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( filtered_sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( sensor_data_filtered["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( sensor_data_filtered["lc" ] )
                    gauge5.setAngle( sensor_data_filtered["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( sensor_data_filtered["pt4"] )
                    gauge8.setAngle( sensor_data_filtered["tc" ] )
                else:
                    gauge1.setText( sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( terminalSerObj.sensor_readouts["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( terminalSerObj.sensor_readouts["lc" ] )
                    gauge5.setAngle( terminalSerObj.sensor_readouts["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( terminalSerObj.sensor_readouts["pt4"] )
                    gauge8.setAngle( terminalSerObj.sensor_readouts["tc" ] )
                update_valve_states( terminalSerObj.valve_states )

                # Log Data
                base_output_filename = output_dir + "/" + engine_state_filenames[liquid_engine_state.state]
                output_filename      = base_output_filename + str( test_num ) + ".txt"
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
                    file.write(str(terminalSerObj.sensor_readouts["lc" ]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["tc" ]) + " ")
                    file.write(terminalSerObj.valve_states["oxPress"  ]   + " ")
                    file.write(terminalSerObj.valve_states["oxVent"   ]   + " ")
                    file.write(terminalSerObj.valve_states["oxPurge"  ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPress"]   + " ")
                    file.write(terminalSerObj.valve_states["fuelVent" ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPurge"]   + " ")
                    file.write(terminalSerObj.valve_states["oxMain"   ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelMain" ]   + " ")
                    file.write("\n")

            ####################################################################
            # Disarm Sequence                                                  #
            ####################################################################
            elif ( liquid_engine_state.get_engine_state() == "Disarm State" ):
                # Check tank pressures
                engineController.tankstat( [], terminalSerObj )

                # Get telemetry
                engineController.telreq( [], terminalSerObj, show_output = False )
                terminalSerObj.sensor_readouts["t"] = time_sec
                sensor_readouts_formatted = {}
                for sensor in terminalSerObj.sensor_readouts:
                    sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                        terminalSerObj.controller,
                        sensor                   ,
                        terminalSerObj.sensor_readouts[sensor] ) 

                # Filter the data
                if ( GAUGE_FILTER_ENABLED ):
                    sensor_data_buffer.add_data( terminalSerObj.sensor_readouts )
                    sensor_data_filtered = sensor_data_buffer.get_data()
                    filtered_sensor_readouts_formatted = {}
                    for sensor in sensor_data_filtered:
                        filtered_sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                            terminalSerObj.controller,
                            sensor                   ,
                            sensor_data_filtered[sensor] ) 

                # Calculate Flow Rates
                if ( GAUGE_FILTER_ENABLED ):
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                sensor_data_filtered["pt1"] -
                                                sensor_data_filtered["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                sensor_data_filtered["pt6"] -
                                                sensor_data_filtered["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )
                else:
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                terminalSerObj.sensor_readouts["pt1"] -
                                                terminalSerObj.sensor_readouts["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                terminalSerObj.sensor_readouts["pt6"] -
                                                terminalSerObj.sensor_readouts["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )

                # Update GUI
                if ( GAUGE_FILTER_ENABLED ):
                    gauge1.setText( filtered_sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( filtered_sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( filtered_sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( filtered_sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( filtered_sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( sensor_data_filtered["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( sensor_data_filtered["lc" ] )
                    gauge5.setAngle( sensor_data_filtered["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( sensor_data_filtered["pt4"] )
                    gauge8.setAngle( sensor_data_filtered["tc" ] )
                else:
                    gauge1.setText( sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( terminalSerObj.sensor_readouts["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( terminalSerObj.sensor_readouts["lc" ] )
                    gauge5.setAngle( terminalSerObj.sensor_readouts["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( terminalSerObj.sensor_readouts["pt4"] )
                    gauge8.setAngle( terminalSerObj.sensor_readouts["tc" ] )
                update_valve_states( terminalSerObj.valve_states )

                # Log Data
                base_output_filename = output_dir + "/" + engine_state_filenames[liquid_engine_state.state]
                output_filename      = base_output_filename + str( test_num ) + ".txt"
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
                    file.write(str(terminalSerObj.sensor_readouts["lc" ]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["tc" ]) + " ")
                    file.write(terminalSerObj.valve_states["oxPress"  ]   + " ")
                    file.write(terminalSerObj.valve_states["oxVent"   ]   + " ")
                    file.write(terminalSerObj.valve_states["oxPurge"  ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPress"]   + " ")
                    file.write(terminalSerObj.valve_states["fuelVent" ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPurge"]   + " ")
                    file.write(terminalSerObj.valve_states["oxMain"   ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelMain" ]   + " ")
                    file.write("\n")

            ####################################################################
            # Post-Fire Engine State                                           #
            ####################################################################
            elif ( liquid_engine_state.get_engine_state() == "Post-Fire State"):
                # Get telemetry
                engineController.telreq( [], terminalSerObj, show_output = False )
                terminalSerObj.sensor_readouts["t"] = time_sec
                sensor_readouts_formatted = {}
                for sensor in terminalSerObj.sensor_readouts:
                    sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                        terminalSerObj.controller,
                        sensor                   ,
                        terminalSerObj.sensor_readouts[sensor] ) 

                # Filter the data
                if ( GAUGE_FILTER_ENABLED ):
                    sensor_data_buffer.add_data( terminalSerObj.sensor_readouts )
                    sensor_data_filtered = sensor_data_buffer.get_data()
                    filtered_sensor_readouts_formatted = {}
                    for sensor in sensor_data_filtered:
                        filtered_sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                            terminalSerObj.controller,
                            sensor                   ,
                            sensor_data_filtered[sensor] ) 

                # Calculate Flow Rates
                if ( GAUGE_FILTER_ENABLED ):
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                sensor_data_filtered["pt1"] -
                                                sensor_data_filtered["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                sensor_data_filtered["pt6"] -
                                                sensor_data_filtered["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )
                else:
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                terminalSerObj.sensor_readouts["pt1"] -
                                                terminalSerObj.sensor_readouts["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                terminalSerObj.sensor_readouts["pt6"] -
                                                terminalSerObj.sensor_readouts["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )

                # Update GUI
                if ( GAUGE_FILTER_ENABLED ):
                    gauge1.setText( filtered_sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( filtered_sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( filtered_sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( filtered_sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( filtered_sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( sensor_data_filtered["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( sensor_data_filtered["lc" ] )
                    gauge5.setAngle( sensor_data_filtered["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( sensor_data_filtered["pt4"] )
                    gauge8.setAngle( sensor_data_filtered["tc" ] )
                else:
                    gauge1.setText( sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( terminalSerObj.sensor_readouts["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( terminalSerObj.sensor_readouts["lc" ] )
                    gauge5.setAngle( terminalSerObj.sensor_readouts["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( terminalSerObj.sensor_readouts["pt4"] )
                    gauge8.setAngle( terminalSerObj.sensor_readouts["tc" ] )
                update_valve_states( terminalSerObj.valve_states )

                # Log Data
                base_output_filename = output_dir + "/" + engine_state_filenames[liquid_engine_state.state]
                output_filename      = base_output_filename + str( test_num ) + ".txt"
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
                    file.write(str(terminalSerObj.sensor_readouts["lc" ]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["tc" ]) + " ")
                    file.write(terminalSerObj.valve_states["oxPress"  ]   + " ")
                    file.write(terminalSerObj.valve_states["oxVent"   ]   + " ")
                    file.write(terminalSerObj.valve_states["oxPurge"  ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPress"]   + " ")
                    file.write(terminalSerObj.valve_states["fuelVent" ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPurge"]   + " ")
                    file.write(terminalSerObj.valve_states["oxMain"   ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelMain" ]   + " ")
                    file.write("\n")

            ####################################################################
            # Manual State                                                     #
            ####################################################################
            elif ( liquid_engine_state.get_engine_state() == "Manual State"):
                # Get telemetry
                engineController.telreq( [], terminalSerObj, show_output = False )
                terminalSerObj.sensor_readouts["t"] = time_sec
                sensor_readouts_formatted = {}
                for sensor in terminalSerObj.sensor_readouts:
                    sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                        terminalSerObj.controller,
                        sensor                   ,
                        terminalSerObj.sensor_readouts[sensor] ) 

                # Filter the data
                if ( GAUGE_FILTER_ENABLED ):
                    sensor_data_buffer.add_data( terminalSerObj.sensor_readouts )
                    sensor_data_filtered = sensor_data_buffer.get_data()
                    filtered_sensor_readouts_formatted = {}
                    for sensor in sensor_data_filtered:
                        filtered_sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                            terminalSerObj.controller,
                            sensor                   ,
                            sensor_data_filtered[sensor] ) 

                # Calculate Flow Rates
                if ( GAUGE_FILTER_ENABLED ):
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                sensor_data_filtered["pt1"] -
                                                sensor_data_filtered["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                sensor_data_filtered["pt6"] -
                                                sensor_data_filtered["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )
                else:
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                terminalSerObj.sensor_readouts["pt1"] -
                                                terminalSerObj.sensor_readouts["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                terminalSerObj.sensor_readouts["pt6"] -
                                                terminalSerObj.sensor_readouts["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )

                # Update GUI
                if ( GAUGE_FILTER_ENABLED ):
                    gauge1.setText( filtered_sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( filtered_sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( filtered_sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( filtered_sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( filtered_sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( sensor_data_filtered["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( sensor_data_filtered["lc" ] )
                    gauge5.setAngle( sensor_data_filtered["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( sensor_data_filtered["pt4"] )
                    gauge8.setAngle( sensor_data_filtered["tc" ] )
                else:
                    gauge1.setText( sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( terminalSerObj.sensor_readouts["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( terminalSerObj.sensor_readouts["lc" ] )
                    gauge5.setAngle( terminalSerObj.sensor_readouts["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( terminalSerObj.sensor_readouts["pt4"] )
                    gauge8.setAngle( terminalSerObj.sensor_readouts["tc" ] )
                update_valve_states( terminalSerObj.valve_states )


            ####################################################################
            # Abort State                                                      #
            ####################################################################
            elif ( liquid_engine_state.get_engine_state() == "Abort State" ):
                # Get telemetry
                engineController.telreq( [], terminalSerObj, show_output = False )
                terminalSerObj.sensor_readouts["t"] = time_sec
                sensor_readouts_formatted = {}
                for sensor in terminalSerObj.sensor_readouts:
                    sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                        terminalSerObj.controller,
                        sensor                   ,
                        terminalSerObj.sensor_readouts[sensor] ) 

                # Filter the data
                if ( GAUGE_FILTER_ENABLED ):
                    sensor_data_buffer.add_data( terminalSerObj.sensor_readouts )
                    sensor_data_filtered = sensor_data_buffer.get_data()
                    filtered_sensor_readouts_formatted = {}
                    for sensor in sensor_data_filtered:
                        filtered_sensor_readouts_formatted[sensor] = SDR_sensor.format_sensor_readout(
                            terminalSerObj.controller,
                            sensor                   ,
                            sensor_data_filtered[sensor] ) 

                # Calculate Flow Rates
                if ( GAUGE_FILTER_ENABLED ):
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                sensor_data_filtered["pt1"] -
                                                sensor_data_filtered["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                sensor_data_filtered["pt6"] -
                                                sensor_data_filtered["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )
                else:
                    ox_flow_rate   = sensor_conv.ox_pressure_to_flow( 
                                                terminalSerObj.sensor_readouts["pt1"] -
                                                terminalSerObj.sensor_readouts["pt2"] )
                    fuel_flow_rate = sensor_conv.fuel_pressure_to_flow(
                                                terminalSerObj.sensor_readouts["pt6"] -
                                                terminalSerObj.sensor_readouts["pt5"] )
                    ox_flow_rate_formatted   = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "oxfr"                   ,
                                                ox_flow_rate   )
                    fuel_flow_rate_formatted = SDR_sensor.format_sensor_readout(
                                                terminalSerObj.controller, 
                                                "ffr"                    , 
                                                fuel_flow_rate )

                # Update GUI
                if ( GAUGE_FILTER_ENABLED ):
                    gauge1.setText( filtered_sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( filtered_sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( filtered_sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( filtered_sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( filtered_sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( sensor_data_filtered["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( sensor_data_filtered["lc" ] )
                    gauge5.setAngle( sensor_data_filtered["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( sensor_data_filtered["pt4"] )
                    gauge8.setAngle( sensor_data_filtered["tc" ] )
                else:
                    gauge1.setText( sensor_readouts_formatted["pt7"], "Fuel Tank Pressure" )
                    gauge2.setText( fuel_flow_rate_formatted        , "Fuel Flow Rate"     )
                    gauge3.setText( "NaN"                           , "None"               )
                    gauge4.setText( sensor_readouts_formatted["lc"] , "Thrust"             )
                    gauge5.setText( sensor_readouts_formatted["pt0"], "LOX Pressure"       )
                    gauge6.setText( ox_flow_rate_formatted          , "LOX Flow Rate"      )
                    gauge7.setText( sensor_readouts_formatted["pt4"], "Engine Pressure"    )
                    gauge8.setText( sensor_readouts_formatted["tc" ], "LOX Temperature"    )
                    gauge1.setAngle( terminalSerObj.sensor_readouts["pt7"] )
                    gauge2.setAngle( fuel_flow_rate                        )
                    gauge3.setAngle( 0 )
                    gauge4.setAngle( terminalSerObj.sensor_readouts["lc" ] )
                    gauge5.setAngle( terminalSerObj.sensor_readouts["pt0"] )
                    gauge6.setAngle( ox_flow_rate                          )
                    gauge7.setAngle( terminalSerObj.sensor_readouts["pt4"] )
                    gauge8.setAngle( terminalSerObj.sensor_readouts["tc" ] )
                update_valve_states( terminalSerObj.valve_states )

                # Log Data
                base_output_filename = output_dir + "/" + engine_state_filenames[liquid_engine_state.state]
                output_filename      = base_output_filename + str( test_num ) + ".txt"
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
                    file.write(str(terminalSerObj.sensor_readouts["lc" ]) + " ")
                    file.write(str(terminalSerObj.sensor_readouts["tc" ]) + " ")
                    file.write(terminalSerObj.valve_states["oxPress"  ]   + " ")
                    file.write(terminalSerObj.valve_states["oxVent"   ]   + " ")
                    file.write(terminalSerObj.valve_states["oxPurge"  ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPress"]   + " ")
                    file.write(terminalSerObj.valve_states["fuelVent" ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelPurge"]   + " ")
                    file.write(terminalSerObj.valve_states["oxMain"   ]   + " ")
                    file.write(terminalSerObj.valve_states["fuelMain" ]   + " ")
                    file.write("\n")


        # Update engine schematic
        plumbing.updatePipeStatus()

        # Draw to main window
        root.update()

        # Draw to plumbing window
        plumbing.getWindow().update()


####################################################################################
# END OF FILE                                                                      #
####################################################################################