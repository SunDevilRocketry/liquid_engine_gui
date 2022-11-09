###### convertDAQ Module:
###### Module for post processing arduino data
###### Post processing prevents unnecessary use of 
###### arduino RAM

## voltage05:
## Input: analogRead value (1-1023)
## Output: voltage (0-5 V)
from os import fstatvfs


def voltage05(x):
	return float(x)*(5.0/1023.0)

## serialFilter:
## Converts strings to floats and filters out null output
## Input: Serial Data
## Output: Float Data
def serialFilter(str):
	try:
		out = float(str)
		return out
	except ValueError:
		return "Null"

## Pressure Transducer Valid?
## Input: PT Serial Number
## Output: 0/1
def PTT(SN):
	if (SN=="test"):
		return 1
	elif (SN=="110718D443"):
		return 1
	elif (SN=="110718D432"):
		return 1
	elif (SN=="112517D435"):
		return 1
	elif (SN=="112517D439"):
		return 1
	elif (SN=="110718D429"):
		return 1
	else:
		return 0

## Pressure Transducer Conversion Code
## Input: PT Serial Number, Voltage
## Output: Pressure
def pressure(SN, v, G):
	if (SN=="test"):
		pressure = v
		return pressure
	elif (SN=="110718D443"):
		v/=G
		pressure = 10602.0*v + 20.83
		return pressure
	elif (SN=="110718D432"):
		v/=G
		pressure = 10131.0*v + 15.21
		return pressure
	elif (SN=="112517D435"):
		v/=G
		pressure = 10234.0*v + 15.73
		return pressure
	elif (SN=="112517D439"):
		v/=G
		pressure = 10122.0*v + 22.22
		return pressure
	elif (SN=="110718D429"):
		v/=G
		pressure = 10188.0*v + 3.42
		return pressure
	else:
		pressure = v
		return pressure

## Flow Rate Calculator
## Input: Pressure drop
## Output: Flow rate
import math 

def Flow(dp):
	# Edit these inputs
	D = 3.0
	d = 1.0
	Cd = 0.5
	rho = 1000.0
	# Do not edit
	pi = math.pi
	beta = d/D 
	A2 = pi*(d/2)**2
	A1 = pi*(D/2)**2
	FR = Cd*((A2/(1.0-beta)**(0.5))*(2.0/rho)**(0.5))*dp**(0.5)
	return FR
