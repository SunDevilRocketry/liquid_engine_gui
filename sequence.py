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

# THREADING METHOD
# Runs in parallel with the GUI main loop
def actionHandler():
    global msg 
    msg = None
    global root, prevCon
    global switch1, switch2, switch3, switch4
    global switch5, switch6, switch7, switch8
    while True:
        time.sleep(0.001)
        if(msg == 'start'):
            '''----------------------------
            ---- STARTUP SEQUENCE HERE ----
            ----------------------------'''

            #TEST SEQUENCE
            delay = 0.2
            delaySlider = 0.001
            if(prevCon): # if Arduino is connected via serial
                for i in range(2):
                    try:
                        print('Trigger Relay 1')
                        switch1.actionOn()
                        time.sleep(delay)
                        for j in range(0, 101, 2):
                            switch7.scale.set(j)
                            time.sleep(delaySlider)
                        for j in range(0, 101, 2):
                            switch7.scale.set(100-j)
                            time.sleep(delaySlider)
                        print('Trigger Relay 2')
                        switch2.actionOn()
                        time.sleep(delay)
                        print('Trigger Relay 3')
                        switch3.actionOn()
                        time.sleep(delay)
                        for j in range(0, 101, 2):
                            switch8.scale.set(j)
                            time.sleep(delaySlider)
                        for j in range(0, 101, 2):
                            switch8.scale.set(100-j)
                            time.sleep(delaySlider)
                        print('Trigger Relay 4')
                        switch4.actionOn()
                        time.sleep(delay)
                        print('Trigger Relay 5')
                        switch5.actionOn()
                        time.sleep(delay)
                        for j in range(0, 101, 2):
                            switch7.scale.set(j)
                            time.sleep(delaySlider)
                        for j in range(0, 101, 2):
                            switch7.scale.set(100-j)
                            time.sleep(delaySlider)
                        print('Trigger Relay 6')
                        switch6.actionOn()
                        time.sleep(delay)
                        print('Trigger Relay 6')
                        switch6.actionOff()
                        time.sleep(delay)
                        print('Trigger Relay 5')
                        switch5.actionOff()
                        time.sleep(delay)
                        print('Trigger Relay 4')
                        switch4.actionOff()
                        time.sleep(delay)
                        print('Trigger Relay 3')
                        switch3.actionOff()
                        time.sleep(delay)
                        print('Trigger Relay 2')
                        switch2.actionOff()
                        time.sleep(delay)
                        print('Trigger Relay 1')
                        switch1.actionOff()
                        time.sleep(delay)
                    except:
                        print('ERROR')
            else:
                print('Serial Error: Arduino Not Connected'
                    + ' or Detected')
                time.sleep(0.1)
