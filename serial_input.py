# Importing Libraries
import serial
import time
bbb = serial.Serial(port='COM7', baudrate=115200, timeout=.1)

def write_read(x):
    bbb.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = bbb.readline()
    return data

while True:
    value = write_read(" hello world ")
    print(value) # printing the value
