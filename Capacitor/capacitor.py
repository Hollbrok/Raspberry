import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt
import math

GPIO.setwarnings(False)

NUMBER_OF_LEDS = 8
bits = [24, 25, 8, 7, 12, 16, 20, 21]

def lightUp(ledNumber, period):
    GPIO.output(bits[ledNumber], GPIO.HIGH)
    time.sleep(period)
    GPIO.output(bits[ledNumber], GPIO.LOW)
    time.sleep(period)

def lightDown(ledNumber, period):
    GPIO.output(bits[ledNumber], GPIO.LOW)
    time.sleep(period)
    GPIO.output(bits[ledNumber], GPIO.HIGH)
    time.sleep(period)

def blink(ledNumber, blinkCount, blinkPeriod):
    for i in range(0, blinkCount):
        lightUp(ledNumber, blinkPeriod)

def runningLight(count, period):
    for i in range(0, count):
        for j in range(0, 8):
           lightUp(j, period) 

def runningDark(count, period):
    GPIO.output(bits, GPIO.HIGH)
    for i in range(0, count):
        for j in range(0, 8):
           lightDown(j, period)
    GPIO.output(bits, 0)


def lightNumber(number):
    binNumber = decToBinList(number)
    #print(binNumber)
    binNumber = binNumber[::-1]
    #print(binNumber)
    #print(bits)
    GPIO.output(bits, binNumber)

def runningPattern(pattern, direction):
    #bitPattern = decToBinList(pattern)
    if(direction):
        while True:
            #print(pattern)
            lightNumber(pattern)
            time.sleep(1)
            #pattern = pattern >> 1
            if(getBit(pattern, 0) == 0):
                pattern = pattern >> 1
            elif(getBit(pattern, 0) == 1):
                pattern = pattern >> 1
                pattern |= 1 << (NUMBER_OF_LEDS - 1)
    elif(direction == 0):
         while True:
            #print(pattern)
            lightNumber(pattern)
            time.sleep(1)
            #pattern = pattern >> 1
            if(getBit(pattern, NUMBER_OF_LEDS - 1) == 0):
                pattern = pattern << 1
            elif(getBit(pattern, NUMBER_OF_LEDS - 1) == 1):
                pattern &= 2 ** (NUMBER_OF_LEDS - 1) - 1
                pattern = pattern << 1
                pattern |= 1

def SHIM(ledNumber, frequency):
    p = GPIO.PWM(bits[ledNumber], frequency)
    p.start(0)
    while True:
        for dc in range(0, 101, 5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -5):
            p.ChangeDutyCycle(dc)
            time.sleep(0.1)
    p.stop()
    GPIO.cleanup()
        
def getBit(number, bit):
    return (number >> bit) & 1


def decToBinList(decNumber) :
    result = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range (0, 8) :
        if (decNumber % 2) == 1 :
            result [i] = 1
        decNumber = decNumber // 2

        if decNumber == 0 :
            return result
    
    return result



#FOR GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup  (bits, GPIO.OUT) # задание канала на выход

lightUp(5, 0)
#GPIO.output(bits, 1)
#blink(1, 4, 1)
#runningLight(2000, 0.1)
#runningDark(5, 0.1)
#print(decToBinList(128))
#lightNumber(16)
#runningPattern(57, 0)
#SHIM(1, 150)





GPIO.setmode(GPIO.BCM)

DAC_PIN_LIST      = [26, 19, 13,  6,  5, 11,  9, 10]
POTENTIOMETR_PIN  = 17
CMP_OUT_PIN       = 4



GPIO.setup(POTENTIOMETR_PIN, GPIO.OUT)
GPIO.setup(DAC_PIN_LIST, GPIO.OUT)
GPIO.setup(CMP_OUT_PIN, GPIO.IN)

DIODS_PIN_LIST = [21, 20, 16, 12,  7,  8, 25, 24]
GPIO.setup(DIODS_PIN_LIST, GPIO.OUT)


def num2dac(number) :
    result = decToBinList(number)
    GPIO.output (DAC_PIN_LIST, 0)

    for i in range (0, 8) :
        if result[i] == 1 :
            GPIO.output(DAC_PIN_LIST [7 - i], 1)

def num2VolLvl(number) :
    vec = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    if (number >= 252):
        vec = [1, 1, 1, 1, 1, 1, 1, 1]
    elif (number > 256 / 8 * 7):
        vec = [0, 1, 1, 1, 1, 1, 1, 1]
    elif (number > 256 / 8 * 6):
        vec  = [0, 0, 1, 1, 1, 1, 1, 1]
    elif (number > 256 / 8 * 5):
        vec  = [0, 0, 0, 1, 1, 1, 1, 1]
    elif (number > 256 / 8 * 4):
        vec  = [0, 0, 0, 0, 1, 1, 1, 1]
    elif (number > 256 / 8 * 3):
        vec  = [0, 0, 0, 0, 0, 1, 1, 1]
    elif (number > 256 / 8 * 2):
        vec  = [0, 0, 0, 0, 0, 0, 1, 1]
    elif (number > 256 / 8 * 1):
        vec  = [0, 0, 0, 0, 0, 0, 0, 1]
    else:
        vec  = [0, 0, 0, 0, 0, 0, 0, 0]

    GPIO.output(DIODS_PIN_LIST, 0)

    for i in range (0, 8) :
        if vec[i] == 1 :
            GPIO.output(DIODS_PIN_LIST [7 - i], 1)

def search() :
    voltage = 0

    for i in range (0, 255) :
        num2dac(i)
        time.sleep(0.001)
        if GPIO.input(CMP_OUT_PIN) != 1 :
            voltage = 3.3 * float(i) / 255
            break
    
    return voltage


def binSearch() :
    value = 0
    i  = 128

    while True :
        num2dac(value)
        time.sleep(0.0005)

        if GPIO.input(CMP_OUT_PIN) == 1 :
            value += i
        else :
            value -= i

        i = int(i / 2)
        if i == 0 :
            break

    if value < 0 :
        return 0
    return value



GPIO.output(POTENTIOMETR_PIN, 1)

value = 0

while True:
    value = binSearch()
    num2VolLvl(value)
    print(value)



GPIO.output(DAC_PIN_LIST, 0)
#GPIO.output(POTENTIOMETR_PIN)
GPIO.cleanup()
