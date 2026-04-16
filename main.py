####################################################################################
#                                                                                  #
# main.py -- application entry point for SDR's liquid engine dashboard             #
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
__hall_of_fame__ = ["Colton Acosta"   ,
               "Katie Herrington",
               "Ian Chandra"      ]
####################################################################################
# Standard Imports                                                                 #
####################################################################################

import time
import os
import datetime
import sys
import serial
import serial.tools.list_ports


####################################################################################
# Project Modules                                                                  #
####################################################################################

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_BASE_DIR, 'plumbing'))
sys.path.insert(0, os.path.join(_BASE_DIR, 'sdec'))

import sdec
import commands
import engineController

from liquid_engine_state import Liquid_Engine_State
from sensor_data_buffer  import Sensor_Data_Buffer
from callbacks           import CallbackHandler
from app_window          import DashboardWindow
from telemetry           import TelemetryProcessor


####################################################################################
# Global State                                                                     #
####################################################################################

liquid_engine_state = Liquid_Engine_State()
sensor_data_buffer  = Sensor_Data_Buffer( tau=1 )

engine_state_filenames = {
    "Initialization State": "init"     ,
    "Ready State"         : "ready"    ,
    "Pre-Fire Purge State": "pfpurge"  ,
    "Fill and Chill State": "fillchill",
    "Standby State"       : "standby"  ,
    "Fire State"          : "fire"     ,
    "Disarm State"        : "disarm"   ,
    "Post-Fire State"     : "postfire" ,
    "Manual State"        : "manual"   ,
    "Abort State"         : "abort"    ,
}


####################################################################################
# Setup functions                                                                  #
####################################################################################

def setup_serial_port( engine_state ):
    """Connect to the first available CP2102 USB device and transition to Ready State.

    Returns the initialised terminalSerObj."""
    terminal = sdec.terminalData()
    for _, port in enumerate( serial.tools.list_ports.comports() ):
        if 'CP2102' in port.description:
            commands.connect( ['-p', port.device], terminal )
            engine_state.set_engine_state( "Ready State" )
    return terminal


def setup_data_logging( engine_state ):
    """Create a dated output directory and find the next unused test-run number.
    Writes an initial marker file for the Initialization State.

    Returns (output_dir, test_num)."""
    run_date   = datetime.date.today().strftime("%m-%d-%Y")
    output_dir = os.path.join("output", "hotfire", run_date)
    os.makedirs(output_dir, exist_ok=True)

    base     = os.path.join(output_dir, engine_state_filenames[engine_state.state])
    test_num = 0
    while os.path.exists( base + str(test_num) + ".txt" ):
        test_num += 1

    with open( base + str(test_num) + ".txt", "a" ) as f:
        f.write( "Initialization State" )

    return output_dir, test_num


####################################################################################
# Main application entry point                                                     #
####################################################################################
if __name__ == '__main__':

    # --- Setup ------------------------------------------------------------------
    terminalSerObj       = setup_serial_port( liquid_engine_state )
    output_dir, test_num = setup_data_logging( liquid_engine_state )

    # --- Wire components --------------------------------------------------------
    exit_flag     = [False]            # mutable container so CallbackHandler can set it
    valve_buttons = {}                 # shared dict; DashboardWindow populates it

    callbacks = CallbackHandler(
        liquid_engine_state, terminalSerObj, valve_buttons, exit_flag
    )
    window = DashboardWindow( callbacks, valve_buttons )
    callbacks.set_window( window )     # break init cycle: window now set on handler

    processor = TelemetryProcessor(
        terminal               = terminalSerObj,
        sensor_buffer          = sensor_data_buffer,
        gauges                 = window.gauges,
        update_valve_fn        = window.update_valve_states,
        engine_state           = liquid_engine_state,
        engine_state_filenames = engine_state_filenames,
        output_dir             = output_dir,
        test_num               = test_num,
        start_time             = time.perf_counter(),
        gauge_filter_enabled   = True,
    )

    # --- Main loop --------------------------------------------------------------
    while not exit_flag[0]:
        if terminalSerObj.comport is None:
            for _, port in enumerate( serial.tools.list_ports.comports() ):
                if ( 'CP2102' in port.description ) or ( 'CP210x' in port.description ):
                    commands.connect( ['-p', port.device], terminalSerObj )
                    liquid_engine_state.set_engine_state( "Ready State" )

        else:
            state = liquid_engine_state.get_engine_state()

            if   state == "Ready State":
                processor.process(show_output=True)
            elif state == "Pre-Fire Purge State":
                processor.process()
            elif state == "Fill and Chill State":
                engineController.tankstat([], terminalSerObj)
                processor.process()
            elif state == "Standby State":
                processor.process()
            elif state == "Fire State":
                processor.process()
            elif state == "Disarm State":
                engineController.tankstat([], terminalSerObj)
                processor.process()
            elif state == "Post-Fire State":
                processor.process()
            elif state == "Manual State":
                processor.process(show_output=True)
            elif state == "Abort State":
                processor.process()

        window.update()

####################################################################################
# END OF FILE                                                                      #
####################################################################################
