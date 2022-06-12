from tkinter import *
import tkinter as tk

pad = 10
width = 60
height = 60
sl_width = 500

class StepperSlider:
    def __init__(self, root, pinNum, arduino):

        self.pinNum = pinNum
        self.arduino = arduino

        self.switch = tk.Frame(root, background='black', width=sl_width, height=height)

        var = DoubleVar()
        self.scale = Scale(self.switch, orient=HORIZONTAL, variable=var, bg='black', fg='white')
        self.scale.bind("<ButtonRelease-1>", self.actionWriteServo)
        self.scale.pack(side='left')
        #self.scale.configure(command=self.actionWriteServo())


        self.switch.pack(side='left', padx=11*pad)


    def setArduino(self, arduino):
        self.arduino = arduino

    def actionWriteServo(self, event):
        val = self.scale.get()
        self.arduino.write(str.encode("S" + str(self.pinNum) + chr(val)))
        print("S" + str(self.pinNum) + chr(val))

    def getFrame(self):
        return self.switch

    def getVal(self):
        return self.scale.get()

class RelayLED:

    def __init__(self, root, background, onB, offB, title, width, height):
        self.c = Canvas(root, width=width, height=height, bg=background, highlightthickness=0)
        self.width = width
        self.height = height

        self.on = onB
        self.off = offB

        #self.stateOutline = self.c.create_oval(3 * width / 8.0, 3 * height / 8.0, 5 * width / 8.0, 5 * height / 8.0, outline='white', width=1)
        self.state = self.c.create_oval((width / 4.0) + 1, (height / 4.0) + 1, (3 * width / 4.0) - 1, (3 * height / 4.0) - 1,
                                               fill=offB)
        self.text = self.c.create_text(width / 2.0, 7 * height / 8.0, font=("Arial", 7, 'bold'), fill="white", text=title)

    def setState(self, state):
        if(state):
            self.c.itemconfig(self.state, fill=self.on)
        else:
            self.c.itemconfig(self.state, fill=self.off)

    def getWidget(self):
        return self.c

class Buttons:
    def __init__(self, root, pinNum, arduino, text, symbol):
        self.arduino = arduino

        self.pinNum = pinNum

        self.symbol = symbol

        self.switch = tk.Frame(root, background = 'black')
        self.led = RelayLED(self.switch, 'black', '#41d94d', '#ed3b3b', text, width, height)
        self.state = 0
        self.off_button = tk.Button(self.switch, text="OFF", width=12, command=self.actionOff, bg='#ed3b3b', fg='white', activebackground='#d42f2f', activeforeground='white')
        self.on_button = tk.Button(self.switch, text="ON", width=12, command=self.actionOn, bg='#41d94d', fg='white', activebackground='#28bd33', activeforeground='white')
        self.off_button.pack(side="right")
        self.led.getWidget().pack(side="right")
        self.on_button.pack(side="right")
        self.switch.pack(side='left', padx=4*pad)

    def setArduino(self, arduino):
        self.arduino = arduino

    def actionOff(self):
        try:
            self.arduino.write(str.encode(str(self.pinNum) + "0"))
            self.led.setState(False)
            self.symbol.setState(False)
            print(str(self.pinNum) + "0 (OFF)")
        except:
            print('Serial Error: Arduino Not Connected or Detected ' + str(self.pinNum))

    def actionOn(self):
        try:
            self.arduino.write(str.encode(str(self.pinNum) + "1"))
            self.led.setState(True)
            self.symbol.setState(True)
            print(str(self.pinNum) + "1 (ON)")
        except:
            print('Serial Error: Arduino Not Connected or Detected ' + str(self.pinNum))

    def setLedState(self, state):
        self.led.setState(state)

    def getFrame(self):
        return self.switch


class Switch:

    def __init__(self, root, name, pinNum, arduino):
        self.arduino = arduino

        self.name = name
        self.pinNum = pinNum


        self.switch = tk.Frame(root)
        self.lR = tk.Label(self.switch, text=name, bg="red", fg="white", font="Arial 16 bold")
        self.state = tk.StringVar(value=0)
        self.off_button = tk.Radiobutton(self.switch, text="OFF", variable=self.state, indicatoron=False, value=0, width=12, command=self.action)
        self.on_button = tk.Radiobutton(self.switch, text="ON", variable=self.state, indicatoron=False, value=1, width=12, command=self.action)
        self.lR.pack(side="left")
        self.off_button.pack(side="left")
        self.on_button.pack(side="left")
        self.switch.pack(pady=pad)

    def action(self):
        serialNum = (self.pinNum*2) + int(self.state.get())
        if (serialNum%2 == 1):
            self.lR.config(bg="green2")
        elif (serialNum%2 == 0):
            self.lR.config(bg="red")
        self.arduino.write(str.encode(str(serialNum)))
        print(str(serialNum))