import arduinoCom as aC 

Ports = aC.getPorts()
print(Ports[0])

NanoPort = aC.findArduinoNano(Ports)
print(NanoPort)