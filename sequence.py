###############################################################
#                                                             #
# sequence.py -- contains functions to implement engine       #
#                sequencing routines                          #
#                                                             #
# Author: Nitish Chennoju, Colton Acosta                      #
# Date: 6/12/2022                                             #
# Sun Devil Rocketry Avionics                                 #
#                                                             #
###############################################################


###############################################################
# Standard Imports                                            #
###############################################################
import time
import sys


###############################################################
# Sequencing Functions                                        #
###############################################################

# method called by button. Message forwarded to 
# threading function
def startup():
    print('startup')

# Hard code all off
# Relays (no power state), Stepper/Servo (pos = 0)
def allOff():
	print('all off')
