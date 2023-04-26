####################################################################################
#                                                                                  #
# sequence.py -- contains functions to implement engine sequencing routines        #
#                                                                                  #
# Author: Nitish Chennoju, Colton Acosta                                           #
# Date: 6/12/2022                                                                  #
# Sun Devil Rocketry Avionics                                                      #
#                                                                                  #
####################################################################################


####################################################################################
# Standard Imports                                                                 #
####################################################################################
import time
import sys


####################################################################################
# Project Imports                                                                  #
####################################################################################
import engineController
import valveController


####################################################################################
# Sequencing Functions                                                             #
####################################################################################


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		pre_fire_purge                                                             #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Initiates the pre-hotfire purge of the engine                              #
#                                                                                  #
####################################################################################
def pre_fire_purge( engine_state, serialObj ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( state != "Ready State" ):
        print( "Error: Cannot perform the pre-fire purge. The engine controller " +
                "must be in the Ready state to perform the purge. The current "   +
                "state is: ")
        print( state )
        return

    # Initiate the pre-fire purge
    engineController.pfpurge( [], serialObj )

    # Set the new engine state
    engine_state.set_engine_state( serialObj.get_engine_state() )
## pre_fire_purge ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		fill_and_chill                                                             #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Initiates the fill and chill engine sequence                               #
#                                                                                  #
####################################################################################
def fill_and_chill( engine_state, serialObj ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( state != "Pre-Fire Purge State" ):
        print( "Error: Cannot initiate the Fill and Chill sequence. The engine " + 
               "controller must be in the Pre-Fire Purge state to initiate the " +
               "Fill and Chill sequence. The current state is: " )
        print( state )
        return

    # Initiate the fill and chill sequence
    engineController.fillchill( [], serialObj )

    # Set the new engine state
    engine_state.set_engine_state( serialObj.get_engine_state() )
## fill_and_chill ## 


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		standby                                                                    #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Puts the engine controller into the standby state                          #
#                                                                                  #
####################################################################################
def standby( engine_state, serialObj ):

    # Verify correct state
    state = engine_state.get_engine_state() 
    if ( state != "Fill and Chill State" ):
        print( "Error: Cannot initiate the standby sequence. The engine controller " +
                "must be in the Fill and Chill state to transition into Standby. The current "   +
                "state is: ")
        print( state )
        return

    # Put the engine in standby state
    engineController.standby( [], serialObj )

    # Set the new engine state
    engine_state.set_engine_state( serialObj.get_engine_state() )
## standby ## 


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		fire_engine                                                                #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Initiates the engine ignition sequence                                     #
#                                                                                  #
####################################################################################
def fire_engine( engine_state, serialObj ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( state != "Standby State" ):
        print( "Error: Cannot initiate the hotfire. The engine controller must " + 
               "be in the Standby state in order to initiate the hotfire. The "  +
               "current state is: ")
        print( state )
        return

    # Initiate the hotfire
    engineController.hotfire( [], serialObj )

    # Set the new engine state
    engine_state.set_engine_state( serialObj.get_engine_state() )
## fire_engine ## 


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		hotfire_abort                                                              #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Aborts the hotfire sequence                                                #
#                                                                                  #
####################################################################################
def hotfire_abort( engine_state, serialObj ):

    # Issue the abort command
    engineController.hotfire_abort( [], serialObj )

    # Set the new engine state
    engine_state.set_engine_state( serialObj.get_engine_state() )
## hotfire_abort ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		get_state                                                                  #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Gets the state of the hotfire                                              #
#                                                                                  #
####################################################################################
def get_state( engine_state, serObj ):
    engineController.hotfire_getstate( [], serObj )
    engine_state.set_engine_state( serObj.get_engine_state() )
## get_state ## 


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		stop_hotfire                                                               #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Stops the engine hotfire                                                   #
#                                                                                  #
####################################################################################
def stop_hotfire( engine_state, serialObj ):

    # Verify correct state
    state = engine_state.get_state()
    if ( state != "Fire State" ):
        print( "Error: Cannot stop the engine hotfire. The engine controller " +
                "must be in the Fire State in order to stop the hotfire. The " +
                "current state is: " )
        print( state )
        return
    
    # Issue the stop hotfire command 
    engineController.stop_hotfire( [], serialObj )
## stop_hotfire ## 


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		stop_purge                                                                 #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Halts the post-hotfire purge                                               #
#                                                                                  #
####################################################################################
def stop_purge( engine_state, serialObj ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( state != "Fire State" ):
        print( "Error: Cannot stop the engine purge. The engine controller " +
                "must be in the Fire State in order to stop the purge. The " +
                "current state is: " )
        print( state )
        return
    
    # Issue the stop purge command
    engineController.stop_purge( [], serialObj )

    # Set the new engine state
    engine_state.set_engine_state( serialObj.get_engine_state() )
## stop_purge ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		kbottle_close                                                              #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Indicate that the kbottle has been closed                                  #
#                                                                                  #
####################################################################################
def kbottle_close( engine_state, serialObj ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( state != "Disarm State" ):
        print( "Cannot send the K-Bottle close command. The engine controller " +
               "must be in the Disarm State in order to issue the command. The " +
               "current state is: " )
        print( state )
        return
    
    # Issue the kbottle close command
    engineController.kbottle_close( [], serialObj )

    # Set the new engine state
    engine_state.set_engine_state( serialObj.get_engine_state() )
## kbottle_close ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		lox_purge                                                                  #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Initiate the LOX tank purge                                                #
#                                                                                  #
####################################################################################
def lox_purge( engine_state, serialObj ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( ( state != "Disarm State" ) and ( state != "Fire State" ) ):
        print( "Cannot send the LOX purge close command. The engine controller " +
               "must be in the Disarm State in order to issue the command. The " +
               "current state is: " )
        print( state )
        return
    
    # Issue the kbottle close command
    engineController.lox_purge( [], serialObj )
## lox_purge ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		manual                                                                     #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Put the engine into manual mode                                            #
#                                                                                  #
####################################################################################
def manual( engine_state, serialObj ):

    # Issue the manual command
    engineController.manual( [], serialObj )

    # Update the engine state
    engine_state.set_engine_state( serialObj.get_engine_state() )
## lox_purge ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		manual_lox_press                                                           #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Manually actuate the LOX pressure solenoid                                 #
#                                                                                  #
####################################################################################
def manual_lox_press( engine_state, serialObj, solenoid_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( ( state != "Manual State" ) ):
        print( "Cannot acutate the LOX pressure valve. The engine controller " +
               "must be in the Manual State in order to issue the command. The " +
               "current state is: " )
        print( state )
        return
    
    # Issue the actuation command
    if ( solenoid_state ):
        # Close solenoid
        valveController.sol( ['close', '-n', 'oxPress'], serialObj )
    else:
        # Open solenoid
        valveController.sol( ['open', '-n', 'oxPress'], serialObj )
## lox_purge ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		manual_fuel_press                                                          #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Manually actuate the Fuel pressure solenoid                                #
#                                                                                  #
####################################################################################
def manual_fuel_press( engine_state, serialObj, solenoid_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( ( state != "Manual State" ) ):
        print( "Cannot acutate the valve. The engine controller " +
               "must be in the Manual State in order to issue the command. The " +
               "current state is: " )
        print( state )
        return
    
    # Issue the actuation command
    if ( solenoid_state ):
        # Close solenoid
        valveController.sol( ['close', '-n', 'fuelPress'], serialObj )
    else:
        # Open solenoid
        valveController.sol( ['open', '-n', 'fuelPress'], serialObj )
## lox_purge ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		manual_lox_vent                                                            #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Manually actuate the LOX vent solenoid                                     #
#                                                                                  #
####################################################################################
def manual_lox_vent( engine_state, serialObj, solenoid_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( ( state != "Manual State" ) ):
        print( "Cannot acutate the valve. The engine controller " +
               "must be in the Manual State in order to issue the command. The " +
               "current state is: " )
        print( state )
        return
    
    # Issue the actuation command
    if ( solenoid_state ):
        # Close solenoid
        valveController.sol( ['close', '-n', 'oxVent'], serialObj )
    else:
        # Open solenoid
        valveController.sol( ['open', '-n', 'oxVent'], serialObj )
## manual_lox_vent ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		manual_fuel_vent                                                           #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Manually actuate the LOX vent solenoid                                     #
#                                                                                  #
####################################################################################
def manual_fuel_vent( engine_state, serialObj, solenoid_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( ( state != "Manual State" ) ):
        print( "Cannot acutate the valve. The engine controller " +
               "must be in the Manual State in order to issue the command. The " +
               "current state is: " )
        print( state )
        return
    
    # Issue the actuation command
    if ( solenoid_state ):
        # Close solenoid
        valveController.sol( ['close', '-n', 'fuelVent'], serialObj )
    else:
        # Open solenoid
        valveController.sol( ['open', '-n', 'fuelVent'], serialObj )
## manual_fuel_vent ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		manual_lox_purge                                                           #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Manually actuate the LOX purge solenoid                                    #
#                                                                                  #
####################################################################################
def manual_lox_purge( engine_state, serialObj, solenoid_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( ( state != "Manual State" ) ):
        print( "Cannot acutate the valve. The engine controller " +
               "must be in the Manual State in order to issue the command. The " +
               "current state is: " )
        print( state )
        return
    
    # Issue the actuation command
    if ( solenoid_state ):
        # Close solenoid
        valveController.sol( ['close', '-n', 'oxPurge'], serialObj )
    else:
        # Open solenoid
        valveController.sol( ['open', '-n', 'oxPurge'], serialObj )
## manual_lox_purge ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		manual_fuel_purge                                                          #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Manually actuate the Fuel purge solenoid                                   #
#                                                                                  #
####################################################################################
def manual_fuel_purge( engine_state, serialObj, solenoid_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( ( state != "Manual State" ) ):
        print( "Cannot acutate the valve. The engine controller " +
               "must be in the Manual State in order to issue the command. The " +
               "current state is: " )
        print( state )
        return
    
    # Issue the actuation command
    if ( solenoid_state ):
        # Close solenoid
        valveController.sol( ['close', '-n', 'fuelPurge'], serialObj )
    else:
        # Open solenoid
        valveController.sol( ['open', '-n', 'fuelPurge'], serialObj )
## manual_fuel_purge ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		manual_lox_main                                                            #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Manually actuate the LOX main valve                                        #
#                                                                                  #
####################################################################################
def manual_lox_main( engine_state, serialObj, valve_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( ( state != "Manual State" ) ):
        print( "Cannot acutate the valve. The engine controller " +
               "must be in the Manual State in order to issue the command. The " +
               "current state is: " )
        print( state )
        return
    
    # Issue the actuation command
    if ( valve_state ):
        # Close solenoid
        valveController.valve( ['close', '-n', 'ox'], serialObj )
    else:
        # Open solenoid
        valveController.valve( ['open', '-n', 'ox'], serialObj )
## manual_lox_main ##


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		manual_fuel_main                                                           #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Manually actuate the main fuel valve                                       #
#                                                                                  #
####################################################################################
def manual_fuel_main( engine_state, serialObj, valve_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( ( state != "Manual State" ) ):
        print( "Cannot acutate the valve. The engine controller " +
               "must be in the Manual State in order to issue the command. The " +
               "current state is: " )
        print( state )
        return
    
    # Issue the actuation command
    if ( valve_state ):
        # Close solenoid
        valveController.valve( ['close', '-n', 'fuel'], serialObj )
    else:
        # Open solenoid
        valveController.valve( ['open', '-n', 'fuel'], serialObj )
## manual_fuel_main ##



####################################################################################
# END OF FILE                                                                      # 
####################################################################################