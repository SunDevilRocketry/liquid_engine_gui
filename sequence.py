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
def pre_fire_purge( engine_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( state != "Ready State" ):
        print( "Error: Cannot perform the pre-fire purge. The engine controller " +
                "must be in the Ready state to perform the purge. The current "   +
                "state is: ")
        print( state )
        return
    ## TODO: Implement
    print( "Pre-fire purge" ) 

    # Set the new engine state
    engine_state.set_engine_state( "Pre-Fire Purge State" )
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
def fill_and_chill( engine_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( state != "Pre-Fire Purge State" ):
        print( "Error: Cannot initiate the Fill and Chill sequence. The engine " + 
               "controller must be in the Pre-Fire Purge state to initiate the " +
               "Fill and Chill sequence. The current state is: " )
        print( state )
        return

    ## TODO: Implement
    print( "Fill and Chill" )

    # Set the new engine state
    engine_state.set_engine_state( "Fill and Chill State" )
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
def standby( engine_state ):

    # Verify correct state
    state = engine_state.get_engine_state() 
    if ( state != "Fill and Chill State" ):
        print( "Error: Cannot initiate the standby sequence. The engine controller " +
                "must be in the Fill and Chill state to transition into Standby. The current "   +
                "state is: ")
        print( state )
        return

    ## TODO: Implement
    print( "Standby" )

    # Set the new engine state
    engine_state.set_engine_state( "Standby State" )
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
def fire_engine( engine_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( state != "Standby State" ):
        print( "Error: Cannot initiate the hotfire. The engine controller must " + 
               "be in the Standby state in order to initiate the hotfire. The "  +
               "current state is: ")
        print( state )
        return

    ## TODO: Implement
    print( "FIRE" )

    # Set the new engine state
    engine_state.set_engine_state( "Fire State" )
## fire_engine ## 


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		disarm                                                                     #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Disarms the engine post hotfire                                            #
#                                                                                  #
####################################################################################
def disarm( engine_state ):

    # Verify correct state
    state = engine_state.get_engine_state()
    if ( state != "Fire State" ):
        print( "Error. Cannot disarm the engine. The engine controller must be " +
               "in the Fire state in order to disarm. The current state is: " )
        print( state )
        return

    ## TODO: Implement
    print( "DISARM" )

    # Set the new engine state
    engine_state.set_engine_state( "Disarm State" )
## disarm ## 


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
# 		hotfire_abort                                                              #
#                                                                                  #
# DESCRIPTION:                                                                     #
# 		Aborts the hotfire sequence                                                #
#                                                                                  #
####################################################################################
def hotfire_abort( engine_state ):
    ## TODO: Implement
    print( "ABORT" )

    # Set the new engine state
    engine_state.set_engine_state( "Abort State" )
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
def get_state( engine_state ):
    ## TODO:Implement
    print( "Getstate" )
## get_state ## 


####################################################################################
# END OF FILE                                                                      # 
####################################################################################