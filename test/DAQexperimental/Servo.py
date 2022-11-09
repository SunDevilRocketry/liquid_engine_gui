__author__ = "Colton Acosta"
__credits__=["Nitish Chennoju"]


# GUI Imports
import tkinter as tk 
import Gauge
from PIL import Image,ImageTk
import numpy as np
from matplotlib import pyplot as plt
import time

# Arduino Imports
from arduinoCom import *
from convertDAQ import *

# Setup GUI
root = tk.Tk()
root.geometry("600x600")
root.title("Analog Voltage Reading")
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

PortFrame =tk.Frame(root)
l1 = tk.Label(PortFrame,text="Connection Status: ",bg="black",fg="white",font="Helvetica 14")


if (UnoPort!="None"):
	l2 = tk.Label(PortFrame,text="Connected ["+UnoPort+"]",bg="black",fg="green",font="Helvetica 14")
	Port = UnoPort
	baudrate = 9600
if (NanoPort!="None"):
	l2 = tk.Label(PortFrame,text="Connected ["+NanoPort+"]",bg="black",fg="green",font="Helvetica 14")	
	Port = NanoPort
	baudrate = 115200
if (UnoPort=="None" and NanoPort=="None"):
	l2 = tk.Label(PortFrame,text="Disconnected",bg="black",fg="red",font="Helvetica 14")
	Port = "None"
	baudrate = 9600

l1.pack(side="left")
l2.pack(side="left")
PortFrame.pack(pady=20)

ServoSlider = tk.Scale(root, from_=0, to=50, orient=tk.HORIZONTAL)
ServoSlider.config(bg='white',bd = 0, length=250, activebackground='green', troughcolor='white', width=40, sliderlength=60, showvalue=False)
ServoSlider.pack(pady=20)

ServoPosition = tk.StringVar()
ServoPosition.set(str(ServoSlider.get()))

ServoLabel = tk.Label(root,text = 'Servo Position: '+ str(ServoPosition.get()) + ' Degrees',bg='black',fg='white', font='Helvetica 12')
ServoLabel.pack()

# Connect to Arduino Serial PortmyServo.write(angle);
serialData = serial.Serial(Port[0:4],baudrate=baudrate)


while True:

	ServoPosition.set(str(ServoSlider.get()))
	ServoLabel.config(text = 'Servo Position: '+ str(ServoPosition.get()) + ' Degrees')

	#serialData.write(ServoSlider.get())

	# Read Data point
	#data = getData(serialData)

	# Convert Data to manageable form
	#dataf = serialFilter(data)

	#print('Data Recieved: '+ data)
	#print('Data Sent: ' +str(ServoSlider.get()))

	root.update()
