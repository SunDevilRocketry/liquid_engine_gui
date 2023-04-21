####################################################################################
#                                                                                  #
# sensor.py -- Contains functions for processing sensor readouts                   #
#                                                                                  #
# Author: Colton Acosta                                                            #
# Date: 1/12/2023                                                                  #
# Sun Devil Rocketry Avionics                                                      #
#                                                                                  #
####################################################################################


####################################################################################
# Imports                                                                          #
####################################################################################
import controller as SDR_controller


####################################################################################
# Imports                                                                          #
####################################################################################
max_sensor_vals = {
                   "pt0"  : 1000, 
                   "pt1"  : 1000, 
                   "pt2"  : 1000,
                   "pt3"  : 1000,
                   "pt4"  : 1000,
                   "pt5"  : 1000,
                   "pt6"  : 1000,
                   "pt7"  : 1000,
                   "tc"   : 100 ,
                   "lc"   : 500 ,
                   "oxfr" : 1.0, 
                   "ffr"  : 1.0
}


####################################################################################
#                                                                                  #
# PROCEDURE:                                                                       #
#         format_sensor_readout                                                    #
#                                                                                  #
# DESCRIPTION:                                                                     #
#        Formats a sensor readout into rounded readout and units                   #
#                                                                                  #
####################################################################################
def format_sensor_readout( controller, sensor, readout ):

    # Readout units
    units = SDR_controller.sensor_units[controller][sensor] 

    # Rounded readout
    if ( units != None ):
        readout_str = "{:.1f}".format( readout )
    else:
        readout_str = str( readout )

    # Concatentate label, readout, and units
    if ( units != None ):
        output = readout_str + " " + units
    else:
        output = readout_str
    return output
## format_sensor_readout ##


###################################################################################
# END OF FILE                                                                     # 
###################################################################################