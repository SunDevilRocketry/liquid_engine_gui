"""
Prototype GUI Interface for Data Aquisition
Displays Analog Voltage of Potentiometer position
Assumes Arduino Uno board is used
Written to be compatible with "DAQexperimental" Arduino script

Last Edit: April 3, 2022
"""

__author__ = "Colton Acosta"
__credits__=["Nitish Chennoju"]
__credits__=["Ian Chandra"]

## USER INPUTS
# Gain
G1 = 51.7   # For P1, A0
G2 = 51.1   # For P2, A5

# Maximum Pressure Expected
pmax = 5

# Maximum Pressure Drop Expect
dpmax = 80

## USER INPUTS

# GUI Imports
import tkinter as tk 
from tkinter import *
# Only for running on mac
from tkmacosx import Button
# Only for running on mac
import Gauge
from PIL import Image,ImageTk
import numpy as np
from matplotlib import pyplot as plt
import time

# Arduino Imports
from arduinoCom import *
from convertDAQ import *

# PT Serial number and Recording on off switch
global PT1S
global PT2S
global rs
rs = 0

# Setup GUI
root = tk.Tk()
root.geometry("800x700")
root.title("Analog Voltage Reading Test")
root.configure(background="black")

# Importing GUI images
SDRlogo = tk.PhotoImage(file='images/SDRLogo5.png')
SDRImage = Image.open("images/SDRlogont2.png")
SDRImage = SDRImage.resize((280,250),Image.ANTIALIAS)
SDR = ImageTk.PhotoImage(SDRImage)
SDRlabel = tk.Label(image=SDR,bg="black")
root.iconphoto(False,SDRlogo)
SDRlabel.pack()

# Display Status of Arduino Uno Connection
UnoPort = findArduinoUno(getPorts())
NanoPort = findArduinoNano(getPorts())
MegaPort = findArduinoMega(getPorts())

PortFrame =tk.Frame(root, bg="black")
PortFrame.pack(pady=0)

l1 = tk.Label(PortFrame,text="Connection Status: ",bg="black",fg="white",font="Helvetica 14")

if (UnoPort!="None"):
	l2 = tk.Label(PortFrame,text="Connected ["+UnoPort+"]",bg="black",fg="green",font="Helvetica 14")
	Port = UnoPort
	baudrate = 9600
elif (NanoPort!="None"):
	l2 = tk.Label(PortFrame,text="Connected ["+NanoPort+"]",bg="black",fg="green",font="Helvetica 14")	
	Port = NanoPort
	baudrate = 115200
elif (MegaPort!="None"):
	l2 = tk.Label(PortFrame,text="Connected ["+MegaPort+"]",bg="black",fg="green",font="Helvetica 14")
	Port = MegaPort
	baudrate = 9600
else:
	l2 = tk.Label(PortFrame,text="Disconnected",bg="black",fg="red",font="Helvetica 14")
	Port = "None"
	baudrate = 9600

l1.pack(side="left")
l2.pack(side="left")

# Start/Stop Recording button Function
dataFilename = 'orificeCalData.txt'
def rst():
    global rs
    global start_time
    if (rs == 1):
        rs = 0
        slabel.configure(text="Not Recording Data", fg = "red")
    elif (rs == 0):
        rs = 1
        slabel.configure(text="Recording Data", fg = "green")
        start_time = time.time()
        # Record Data to txt file
        with open(dataFilename, "w") as file:
            file.write("Time(s) PT1(psi) PT2(psi) DP(psi)\n")

# Start/Stop button and label
sButton = Button(root, text="Start/Stop Recording",font="Helvetica 14", bg="black", bd=0, fg="white", command=rst)
sButton.pack()

slabel = tk.Label(root, text="Data Recording Status", bg="black", fg="white", font="Helvetica 14",highlightbackground = "black", highlightcolor = "black", highlightthickness=2)
slabel.pack()

# PT Entry 1
Entry1Frame = tk.Frame(root, bg="black")
Entry1Frame.pack(pady=0)

Ent1Label = tk.Label(Entry1Frame, text="Enter PT 1 Serial Number:", bg="black", fg="white",font="Helvetica 14")
Ent1Label.pack(side="left")
Ent1 = Entry(Entry1Frame, bg="black", fg="white", highlightbackground="white", highlightcolor = "black", bd=1,font="Helvetica 14", highlightthickness=1)
Ent1.pack(side="left")

def Enter1():
	global PT1SN
	PT1S = Ent1.get()
	PTS = PTT(PT1S)
	if (PTS == 1):
		PT1Label.configure(text="PT 1 Serial Number: " + Ent1.get())
		Ent1.delete(0, END)
		Ent1.insert(0, "")
		PT1SN = PT1S
	else:
		PT1Label.configure(text="PT 1 Serial Number Not Valid ")
		Ent1.delete(0, END)
		Ent1.insert(0, "")
		
Button1 = Button(Entry1Frame, text="Input",font="Helvetica 14", bg="black", bd=0, fg="white", command=Enter1)
Button1.pack(side="left",padx=10)

# PT Entry 2
Entry2Frame = tk.Frame(root, bg="black")
Entry2Frame.pack(pady=0)

EntLabel = tk.Label(Entry2Frame, text="Enter PT 2 Serial Number:", bg="black", fg="white",font="Helvetica 14")
EntLabel.pack(side="left")
Ent2 = Entry(Entry2Frame, bg="black", fg="white", highlightbackground="white", highlightcolor = "black", bd=1,font="Helvetica 14", highlightthickness=1)
Ent2.pack(side="left")

PT2SN = 0
def myClick():
    global PT2SN
    PT2S = Ent2.get()
    PTS = PTT(PT2S)
    if (PTS == 1):
        PT2Label.configure(text="PT 2 Serial Number: " + Ent2.get())
        Ent2.delete(0, END)
        Ent2.insert(0, "")
        PT2SN = PT2S
    else:
        PT2Label.configure(text="PT 2 Serial Number Not Valid ")
        Ent2.delete(0, END)
        Ent2.insert(0, "")
	
Button1 = Button(Entry2Frame, text="Input",font="Helvetica 14", bg="black", bd=0, fg="white", command=myClick)
Button1.pack(side="left",padx=10)

# PT Labels
PTFrame = tk.Frame(root, bg="black")
PTFrame.pack(pady=10)

PT1Label = tk.Label(PTFrame, width= 50, text="Currently Displaying Voltage", bg="black", fg="white", font="Helvetica 14",highlightbackground = "white", highlightcolor = "white", highlightthickness=2)
PT1Label.pack(side="left",padx=15)
PT2Label = tk.Label(PTFrame, width= 50, text="Currently Displaying Voltage", bg="black", fg="white", font="Helvetica 14",highlightbackground = "white", highlightcolor = "white", highlightthickness=2)
PT2Label.pack(side="left",padx=15)

# Insert Gauges
GaugeFrame = tk.Frame(root, bg="black")
GaugeFrame.pack(pady=30)

PressureGage1 = Gauge.Gauge(GaugeFrame,"black",pmax)
PressureGage1.setText("Start","Pressure 1")
PressureGage1.getWidget().pack(side="left", padx=(20,20))

PressureGage2 = Gauge.Gauge(GaugeFrame,"black",pmax)
PressureGage2.setText("Start","Pressure 2")
PressureGage2.getWidget().pack(side="left", padx=(20,20))

FlowRateGage3 = Gauge.Gauge(GaugeFrame,"black",dpmax)
FlowRateGage3.setText("Start","Pressure Drop")
FlowRateGage3.getWidget().pack(side="left", padx=(20,20))

# Connect to Arduino Serial Port
# mac
#serialPortDir = '/dev/usbmodem14301'
# linux
serialPortDir = '/dev/ttyACM0'

serialData = serial.Serial(serialPortDir, baudrate=baudrate,timeout=1)

# Initialize PTSN
PT1SN = 0
PT2SN = 0

# Start Live GUI
start_time = time.time()
while True:
    # Read Data point
    data = getData(serialData)

    # Split the data
    data = data.split(" ")

    if (len(data)==3):
        # Extract time and voltages
        dat1 = int(data[0]) # time
        dat2 = int(data[1]) # v1
        dat3 = int(data[2]) # v2
    else:
        data = "Null"

    if (data!="Null"):

        # Convert to voltage
        t = time.time() - start_time
        v1 = voltage05(dat2)
        v2 = voltage05(dat3)

        # Round Voltage
        voltformat1 = "{:.3f}".format(v1)
        voltformat2 = "{:.3f}".format(v2)

        # Calculate Pressure
        p1 = pressure(PT1SN, v1, G1)
        p2 = pressure(PT2SN, v2, G2)

        # Calculate Flow Rate
        FR = p1 - p2
        #FR = Flow(dp)

        p1format = "{:.3f}".format(p1)
        p2format = "{:.3f}".format(p2)
        FRformat = "{:.3f}".format(FR)

        # Record Data
        if (rs == 1):
            with open(dataFilename, "a") as file:
                file.write(str(t) + " ")
                file.write(str(p1) + " ")
                file.write(str(p2) + " ")
                file.write(str(FR) + "\n")

        # Reconfigure Gauge
        PressureGage1.setAngle(p1)
        PressureGage1.setText(p1format,"Pressure 1 (psi)")

        PressureGage2.setAngle(p2)
        PressureGage2.setText(p2format,"Pressure 2 (psi)")

        FlowRateGage3.setAngle(FR)
        FlowRateGage3.setText(FRformat,"Pressure Difference (psi)")

        # Update
        root.update()

    root.update()
