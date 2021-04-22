
import RPi.GPIO as GPIO
import time
import math
import numpy as np
import matplotlib.pyplot as plt
from time import sleep


NUMBER_OF_LEDS = 8
bits = [10, 9, 11, 5, 6, 13, 19, 26]

def decToBinList(decNumber):
    N = NUMBER_OF_LEDS - 1
    p = 0
    binNumber = []

    while N > 0:
        p = int(decNumber / 2 ** N)
        if p == 1:
            binNumber.append(1)
            decNumber -= 2 ** N
        else:
            binNumber.append(0)
        N -= 1
    binNumber.append(decNumber)
    return binNumber

def lightNumber(number):
    binNumber = decToBinList(number)
    #print(binNumber)
    binNumber = binNumber[::-1]
    GPIO.output(bits, binNumber)


def num2dac(value):
    lightNumber(value)


def firstScript():
    while True:
        print("Введите число(-1 для выхода):")
        value = int(input())
        if ((value == -1) or (value > 255) or (value < 0)):
            print("value =", value)
            break
        else :
            num2dac(value)


def secondScript():
    print("Введите число повторений:")
    repetitionsNumber = int(input())
    if (repetitionsNumber < 1):
        print("repetitionsNumber =", repetitionsNumber)
    else :
        for i in range(repetitionsNumber): # равносильно инструкции for i in 0, 1, ... , repetitionsNumber - 1:
            for j in range(256):
                num2dac(j)
                time.sleep(0.1)
            for j in range(256):
                num2dac(256 - j)
                time.sleep(0.1)
        

def thirdScript():
    print("Введите время работы лампочки:")
    time_light = int(input())
    
    print("Введите frequency()")
    frequency = int(input())

    print("Введите samplingFrequency:")
    samplingFrequency = int(input())

    ndarray = np.arange(0, time_light, 1/samplingFrequency)

    amplitude = np.sin(ndarray*(frequency)*math.pi*2) + 1

    print(ndarray)
    print(amplitude)
    

    for i in range (time_light*samplingFrequency):
        num2dac(round(255 * amplitude[i] / 2))
        time.sleep(1/samplingFrequency)

    plt.plot(ndarray, amplitude)
    plt.show()


def lastScript():
    from scipy.io import wavfile
    data = float(1)
    samplerate, data = wavfile.read('SOUND.WAV') # samplerate - частота дискретизации, дата - массив со всеми данными
    print("samplerate = ",samplerate)
    #print("data:",data)

    duration_seconds = len(data) / float(samplerate)
    print("Длительность аудиофайла = ", duration_seconds)

    y = data[:,0]
    print(y)
    x = np.arange(0, duration_seconds, 1/samplerate)
    print(x)

    for i in range (round(duration_seconds)*samplerate):
        num2dac(round(255 * abs(y[i])))
        time.sleep(1/samplerate)

    plt.plot(x, y)
    plt.show()



GPIO.setmode(GPIO.BCM)
GPIO.setup(bits, GPIO.OUT) # задание канала на выход
GPIO.output(bits, GPIO.LOW) # 


#firstScript()
#secondScript()
#thirdScript()
lastScript()


