import RPi.GPIO as GPIO
import time

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


print ("Введите число повторений:")

repetitionsNumber = int (input ()) 

for i in range (0, repetitionsNumber) :
    for j in range (0, 255) :
        num2dac (j)
        time.sleep(0.01)
    for j in range (255, 0, -1):
        num2dac (j)
        time.sleep(0.01)

GPIO.output (chan_list_dac, 0)
GPIO.cleanup ()