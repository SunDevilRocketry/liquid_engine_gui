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

# Arduino Imports
from arduinoCom import *
from convertDAQ import *

# Setup GUI
root = tk.Tk()
root.geometry("800x800")
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

# Entry
EntryFrame = tk.Frame(root, bg="black")
EntryFrame.pack(pady=0)

EntLabel = tk.Label(EntryFrame, text="Enter PT 1 Serial Number:", bg="black", fg="white",font="Helvetica 14")
EntLabel.pack(side="left")
Ent = Entry(EntryFrame, bg="black", fg="white", highlightbackground="white", highlightcolor = "black", bd=1,font="Helvetica 14", highlightthickness=1)
Ent.pack(side="left")

def myClick():
    global x
    myLabel.configure(text=Ent.get())
    x = int(Ent.get())

def myTest():  
    global x
    print(x)

Button1 = Button(EntryFrame, text="Input",font="Helvetica 14", bg="black", bd=0, highlightbackground = "black", highlightcolor = "black", fg="white", command=myClick, highlightthickness=1)
Button1.pack(side="left",padx=10)

Button2 = Button(EntryFrame, text="Input",font="Helvetica 14", bg="black", bd=0, highlightbackground = "black", highlightcolor = "black", fg="white", command=myTest, highlightthickness=1)
Button2.pack(side="left",padx=10)

# Insert Gauges
GaugeFrame = tk.Frame(root, bg="black")
GaugeFrame.pack(pady=30)

VoltageGage1 = Gauge.Gauge(GaugeFrame,"black",5.0)
VoltageGage1.setText("Start","Voltage 1")
VoltageGage1.getWidget().pack(side="left", padx=(20,20))

VoltageGage1 = Gauge.Gauge(GaugeFrame,"black",5.0)
VoltageGage1.setText("Start","Voltage 2")
VoltageGage1.getWidget().pack(side="left", padx=(20,20))

VoltageGage1 = Gauge.Gauge(GaugeFrame,"black",5.0)
VoltageGage1.setText("Start","Flow Rate")
VoltageGage1.getWidget().pack(side="left", padx=(20,20))

myLabel = tk.Label(root, text="PT 1 Serial Number", bg="black", fg="white",font="Helvetica 14")
myLabel.pack(pady=0)

root.mainloop()


