import RPi.GPIO as GPIO
import time
import math
import numpy as np
import matplotlib.pyplot as plt
import datetime

GPIO.setmode (GPIO.BCM)

chan_list_dac = [26, 19, 13,  6,  5, 11,  9, 10]
GPIO.setup   (chan_list_dac, GPIO.OUT)

def decToBinList( decNumber ) :
    vector = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range (0, 8) :
        if (decNumber % 2) == 1 :
            vector [i] = 1
        decNumber = decNumber // 2

        if decNumber == 0 :
            return vector
    
    return vector

def num2dac( number ) :
    vector = decToBinList (number)
    GPIO.output (chan_list_dac, 0)

    for i in range (0, 8) :
        if vector[i] == 1 :
            GPIO.output (chan_list_dac [7 - i], 1)

print ('freq:')
frequency = int (input ())
print ('sampling freq:')
samplingFrequency = int (input ())
print ('time:')
maxT = int (input ())


sinValsNum = 512
times = np.arange (0, maxT, 1 / samplingFrequency)
amplitude = np.sin (times * frequency * 2 * math.pi)
plt.plot (times, amplitude)
plt.title ('Синус')
plt.xlabel ('Время')
plt.ylabel ('Амплитуда sin(time)')
plt.show ()

initT = time.time()

vals = np.arange (0, int (samplingFrequency * maxT), 1)

for i in range (0, samplingFrequency * maxT) :
    vals[i] = int ((amplitude [i % sinValsNum] + 1) * 128)

for i in range (0, samplingFrequency * maxT) :
    num2dac (vals[i])
    time.sleep (1/samplingFrequency)

GPIO.output (chan_list_dac, 0)
GPIO.cleanup ()