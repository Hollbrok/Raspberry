import RPi.GPIO as GPIO
import time
import math

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
    binNumber = binNumber[::-1]
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


GPIO.setmode(GPIO.BCM)
GPIO.setup  (bits, GPIO.OUT) # задание канала на выход
GPIO.output (bits, GPIO.LOW)		 # 

#lightUp(5, 1)
#GPIO.output(bits, 1)
#blink(1, 4, 1)
#runningLight(2000, 0.1)
#runningDark(5, 0.1)
#print(decToBinList(128))
#lightNumber(16)
#runningPattern(157, 0)
#SHIM(1, 150)
