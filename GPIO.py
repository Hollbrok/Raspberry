import RPi.GPIO as GPIO
import time
import math

def lightUp(ledNumber, period):
    GPIO.output(bits[ledNumber], 1)
    time.sleep(period)
    GPIO.output(bits[ledNumber], 0)
    time.sleep(period)

def lightDown(ledNumber, period):
    GPIO.output(bits[ledNumber], 0)
    time.sleep(period)
    GPIO.output(bits[ledNumber], 1)
    time.sleep(period)

def blink(ledNumber, blinkCount, blinkPeriod):
    for i in range(0, blinkCount):
        lightUp(ledNumber, blinkPeriod)

def runningLight(count, period):
    for i in range(0, count):
        for j in range(0, 8):
           lightUp(j, period) 

def runningDark(count, period):
    GPIO.output(bits, 1)
    for i in range(0, count):
        for j in range(0, 8):
           lightDown(j, period)
    GPIO.output(bits, 0)

def decToBinList(decNumber):
    N = 7
    p = 0
    X = []

    while N > 0:
        p = int(decNumber/2**N)
        if p == 1:
            X.append(1)
            decNumber -= 2**N
        else:
            X.append(0)
        N -= 1
    X.append(decNumber)
    return X

def lightNumber(number):
    x = decToBinList(number)
    x = x[::-1]
    GPIO.output(bits, x)

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
                pattern |= 1 << 7
    elif(direction == 0):
         while True:
            #print(pattern)
            lightNumber(pattern)
            time.sleep(1)
            #pattern = pattern >> 1
            if(getBit(pattern, 7) == 0):
                pattern = pattern << 1
            elif(getBit(pattern, 7) == 1):
                pattern &= 127
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



GPIO.setmode(GPIO.BCM)

bits = [24, 25, 8, 7, 12, 16, 20, 21]
GPIO.setup(bits, GPIO.OUT)

#lightUp(5, 1)
#GPIO.output(bits, 1)
#blink(1, 4, 1)
#runningLight(2000, 0.1)
#runningDark(5, 0.1)
#print(decToBinList(128))
#lightNumber(16)
#runningPattern(157, 0)
GPIO.output(bits, 0)
SHIM(1, 150)
