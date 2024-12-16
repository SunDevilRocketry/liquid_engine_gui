####### arduinoCom Module: Functions for Arduino Communications 

# Arduino imports
import serial
import serial.tools.list_ports as list_ports 


## getPorts: 
## Returns list of accesible serial ports
def getPorts():
	portData = list_ports.comports()
	return portData 

## findArduinoUno:
## Input: list of accesible ports
## Output: COM port of Arduino Uno as String
def findArduinoUno(ports):
	for port in ports:
		if ('ttyACM1' in str(port)):
			return str(port)
	return "None"

## findArduinoNano
## Input: list of accesible ports
## Output: port of arduino Nano
def findArduinoNano(ports):
	for port in ports:
		if ('CH340' in str(port)):
			return str(port)
	return "None"

## findArduinoMega
## Input: list of usable ports
## Output: port of arduino Mega
def findArduinoMega(ports):
	for port in ports:
		if ('Mega' in str(port)):
			return str(port)
	return "None"



## getData:
## Output: Serial Data Point
def getData(serialData):
    Data = serialData.readline()
    try:
        return(Data.decode('utf-8'))
    except UnicodeDecodeError:
        return "Null"


