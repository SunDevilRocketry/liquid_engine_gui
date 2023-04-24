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
    state = engine_state.get_state()
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
# END OF FILE                                                                      # 
####################################################################################