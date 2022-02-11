# Importing Libraries
import serial
import time
bbb = serial.Serial(port='COM8', baudrate=115200, timeout=.1)

def write_read(x):
    bbb.write(bytes(x, 'utf-8'))
    time.sleep(5)
    data = bbb.readline()
    return data

start = time.time()

while True:

    if (time.time() - start > 5):
        bbb.write(bytes('T', 'utf-8'))
        start = time.time()
    
    data = bbb.readline()
    if data:
        print(data)
