# !/usr/bin python3

__author__ = "Nitish Chennoju"

import threading
import time
import serial
import serial.tools.list_ports
from serial import SerialException
import tkinter as tk
from mttkinter import mtTkinter

# Custom Classes
import Gauge
import RelaySwitch
import PandID

msg = ''


# Returns list of all accessible serial ports
def getPorts():
    portData = serial.tools.list_ports.comports()
    return portData

# Returns COM port of Arduino if detected by computer. User for switchbox
def findArduino(portsFound):
    numConnections = len(portsFound)
    for i in range(0, numConnections):
        if ('Uno' in str(portsFound[i]) or 'Nano' in str(portsFound[i]) or 'CH340' in str(portsFound[i])):
            return str(portsFound[i])
    return "None"


def conv(str):
    return str[2:len(str) - 5]

# method called by button. Message forwarded to threading function
def startup():
    global msg
    msg = 'start'
    time.sleep(0.1)
    msg = ''


# Hard code all off
# Relays (no power state), Stepper/Servo (pos = 0)
def check():
    plumbing.one.setState(True)
    plumbing.two.setState(True)

# Hard code all off
# Relays (no power state), Stepper/Servo (pos = 0)
def allOff():
    try:
        arduinoSwitchbox.write(b'8')
        switch1.actionOff()
        time.sleep(0.001)
        print("All OFF COMPLETE")
    except:
        print('Serial Error: Arduino Not Connected or Detected')
    switch1.setLedState(False)

    plumbing.one.setState(False)
    plumbing.two.setState(False)

# THREADING METHOD
# Runs in parallel with the GUI main loop
def actionHandler():
    global msg
    global root, switch1, switch2, switch3, switch4, switch5, switch6, switch7, switch8, prevCon
    while True:
        time.sleep(0.001)
        if(msg == 'start'):
            '''----------------------------
            ---- STARTUP SEQUENCE HERE ----
            ----------------------------'''

            #TEST SEQUENCE
            delay = 0.2
            if(prevCon):
                for i in range(1):
                    try:
                        print('Trigger Relay 1')
                        switch1.actionOn()
                        time.sleep(delay)
                        print('Trigger Relay 1')
                        switch1.actionOff()
                        time.sleep(delay)
                        print('Trigger Relay 1')
                        switch1.actionOn()
                        time.sleep(delay)
                        print('Trigger Relay 1')
                        switch1.actionOff()
                        time.sleep(delay)
                        print('Trigger Relay 1')
                        switch1.actionOn()
                        time.sleep(delay)
                        print('Trigger Relay 1')
                        switch1.actionOff()
                        time.sleep(delay)
                    except:
                        print('ERROR')
            else:
                print('Serial Error: Arduino Not Connected or Detected')
                time.sleep(0.1)








if __name__ == '__main__':
    global root, switch1, switch2, switch3, switch4, switch5, switch6, switch7, switch8, a, b, c, d, off, g1, g2, g3, g4, connectionLabel, plumbing, fileName, arduinoSwitchbox, prevCon

    #ACTION HANDLER THREAD (checks for startup button press)
    thread = threading.Thread(target=actionHandler)
    thread.start()

    # Get file name from user
    print("Enter file name (don't include file extension): ", end='')
    fileName = input() + ".txt"

    # Spacing constants within GUI
    pad = 10
    gridLen = 125

    # Initialize GUI Windows
    plumbing = PandID.Solids_Engine_Plumbing(gridLen)  # P&ID diagram window

    root = tk.Tk(mt_debug = 1)
    root.title("SDR - Solids Dashboard");
    root.configure(background="black")

    tk.Label(root, text="SDR - Solids Dashboard", bg="black", fg="white", font="Arial 30").pack(pady=40)

    # GET ARDUINO STATUS / Update on GUI connection label
    status = findArduino(getPorts())
    connectionLabel = tk.Label(root, text='DISCONNECTED ' + status, bg="black", fg="#ed3b3b", font="Arial 14")
    arduinoSwitchbox = serial.Serial()
    if (not (status == "None")):
        arduinoSwitchbox = serial.Serial(status.split()[0], 115200)
        connectionLabel.configure(text='CONNECTED ' + status, fg="#41d94d")
    connectionLabel.pack()

    # RELAY Switches created
    a = tk.Frame(root, bg='black')  # represents row 1
    switch1 = RelaySwitch.Buttons(a, 0, arduinoSwitchbox, "Igniter", plumbing.one)

    # attaches rows to root tkinter GUI
    a.pack()

    g = tk.Frame(root)
    h = tk.Frame(root)
    check = tk.Button(root, text="CHECK", padx=30, pady=5, font="Arial 14", bg="#41d94d", command=check,
                  activebackground="#41d94d")
    s = tk.Button(root, text="STARTUP", padx=30, pady=5, font="Arial 14", bg="yellow", command=startup,
                  activebackground="yellow")
    off = tk.Button(root, text="E-OFF", padx=25, pady=5, font="Arial 14", bg="RED", command=allOff,
                    activebackground="RED")

    check.pack(pady=pad)
    s.pack(pady=pad)
    off.pack(pady=pad)

    # ------------------------ DATA LOGGER GAUGE ELEMENTS -----------------------------
    # consists of two rows of 2 gauges
    g1 = Gauge.Gauge(g, 'black', 5)
    g1.setText("Nan", "Pressure Trans")
    g1.getWidget().pack(side="left")
    g.pack()


    '''----------------------------
    ------ MAIN PROGRAM LOOP ------
    ----------------------------'''
    prevCon = True
    while True:
        # ARDUINO CONNECTION CHECK
        status = findArduino(getPorts())
        if (status == "None"):
            connectionLabel.configure(text='DISCONNECTED ' + status, fg="#ed3b3b")
            g1.setText("Nan", "Pressure Trans")
            prevCon = False
        elif (not prevCon and status != 'None'):
            try:
                arduinoSwitchbox = serial.Serial(status.split()[0], 115200)
                time.sleep(5)
                connectionLabel.configure(text='CONNECTED ' + status, fg="#41d94d")
                switch1.setArduino(arduinoSwitchbox)
                prevCon = True
            except SerialException:
                print("ERROR: LOADING...")
        else:
            connectionLabel.configure(text='CONNECTED ' + status, fg="#41d94d")


        # Attempt to get data from Arduino
        serialRaw = ''
        try:
            file = open(fileName, "a")
            serialRaw = str(arduinoSwitchbox.readline())
            strSerial = conv(serialRaw)
            file.write(strSerial.replace("\\t", "\t") + "\n")
            file.close()
        except SerialException:
            strSerial = ''
            serialRaw = ''#

        data = strSerial.split("\\t")

        if (data[0] == "Time"):
            print('-------- BEGIN --------')
        elif (len(data) > 1 and data[0] != "Time"):
            g1.setAngle(abs(5 * float(data[1])) / 1023.0)
            g1.setText(data[1].replace('\n', ''), "Pressure Trans")

        root.update()
        plumbing.getWindow().update()