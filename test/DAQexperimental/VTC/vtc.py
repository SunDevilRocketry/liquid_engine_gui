## Transimpedance Amplifier Voltage Transfer Characteristic (VTC) 
import numpy as np
import math
from matplotlib import pyplot as plt

# Circuit Parameters
Vbias = 12 # volts
Vdd = 15 # volts
Rd = 2_000 # ohms
kn = 5.99e-3*(2.5/0.5) # A/V^3
Vbias = 12 # volts
G = 5 # gain
Vt = 0.21 # volts
lamb = 0.00

# input and output vectors
Voff = np.linspace(0.1, Vbias, 10000)
Vout = np.zeros(Voff.shape)
Id = np.zeros(Voff.shape)

# function for vtc
def tiaVTC(Voff, vt, kn, Vbias, Rd, G, lamb): 
    #    ids = (Vbias - Voff)/Rd
    Vtrans = (-1+math.sqrt(1+2*kn*Rd*Vbias))/(kn*Rd)
    if (Vbias == Voff):
        return 0
    elif (Voff >= Vtrans): # Saturation
        return (G*(vt + math.sqrt( (2/(kn*Rd)) * ((Vbias-Voff)/(1+lamb*Voff)))))
    else: # triode
        return (G*(vt +0.5*Voff + Vbias/(kn*Voff*Rd) -1/(kn*Rd)))

# function for current voltage characteristic
def transIV(ids, vt, kn, Vbias, Rd, G):
    Vtrans = (-1+math.sqrt(1+2*kn*Rd*Vbias))/(kn*Rd)
    itrans = 0.5*kn*(Vtrans**2)
    if (ids == 0):
        return 0
    elif (ids < itrans): # saturation
        return (G*(vt + math.sqrt(2*ids/kn)))
    else: 
        return (G*(vt + 0.5*Vbias - 0.5*ids*Rd + Vbias/(kn*Rd*(Vbias - ids*Rd)) -1/(kn*Rd)))

# function for small signal transimpedance
def calcZ(ids, vt, kn, Vbias, Rd, G):
    Vtrans = (-1+math.sqrt(1+2*kn*Rd*Vbias))/(kn*Rd)
    itrans = 0.5*kn*(Vtrans**2)
    if (ids == 0):
        return 0
    elif (ids < itrans): # saturation
        return (G*math.sqrt(1/(2*kn*ids)))
    else: 
        return (G*(Vbias/(kn*(Vbias-ids*Rd)**2) - 0.5*Rd))

# Fill Vout and Id
for i, v in enumerate(Voff):
    Vout[i] = tiaVTC(v, Vt, kn, Vbias, Rd, G, lamb)
    Id[i] = 1000*(Vbias-v)/Rd


# read spice results
with open("spice_sim.csv") as file: 
    lines = file.readlines()

Voff_string_dirt = lines[0].split(";")
Vout_string_dirt = lines[1].split(";")
Voff_string = Voff_string_dirt[1:-2]
Vout_string = Vout_string_dirt[1:-2]
Voff_spice = np.zeros(len(Voff_string))
Vout_spice = np.zeros(len(Vout_string))

# Fill Data from spice simulation
for i, data in enumerate(Voff_string):
    Voff_spice[i] = float(Voff_string[i])
    Vout_spice[i] = float(Vout_string[i])

# plot output
plt.figure()
plt.plot(Voff, Vout)
plt.plot(Voff_spice, Vout_spice)
plt.xlabel("Offset Voltage, V")
plt.ylabel("Output Voltage, V")
plt.title("TIA Voltage Transfer Characteristic")
plt.legend(["Hand Calc", "Simulation"])
plt.grid()
plt.ylim([0,15])
#plt.show()

# plot drain current verus output voltage
Ids = np.linspace(0, 6e-3, 1000)
Vout_i = np.zeros(Ids.shape)
transZanal = np.zeros(Ids.shape)
for i, ids in enumerate(Ids):
    Vout_i[i] = transIV(ids, Vt, kn, Vbias, Rd, G)
    transZanal[i] = calcZ(ids, Vt, kn, Vbias, Rd, G)
    transZanal[i] /= 1000 
    Ids[i] *= 1000

plt.figure()
plt.plot(Id, Vout)
plt.xlabel("Drain Current (mA)")
plt.ylabel("Amplifier Output (V)")
plt.title("Transimpedance Transfer Characteristic")
plt.ylim([0, 12])
plt.grid()
#plt.show()

# Calculate Transimpedances
transZ = np.zeros(Id.shape) # kOhm
transZ[0] = (Vout[1]-Vout[0])/(Id[1]-Id[0])
transZ[-1] = (Vout[-1]-Vout[-2])/(Id[-1]-Id[-2])
nPoints = len(transZ) -1 
for i in range(1, nPoints):
    transZ[i] = (Vout[i+1] - Vout[i-1])/(Id[i+1]-Id[i-1])


# Plot Results
plt.figure()
plt.plot(Id[:-2], transZ[:-2])
plt.plot(Ids, transZanal)
plt.title("Amplifier Transimpedance")
plt.xlabel("Drain Current (mA)")
plt.ylabel("Transimpedance (kOhm)")
plt.legend(['Numerical Result', "Analytical Result"])
plt.ylim([0, 50])
plt.grid()
plt.show()
