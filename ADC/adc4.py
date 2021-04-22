import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

DAC_PIN_LIST      = [26, 19, 13,  6,  5, 11,  9, 10]
POTENTIOMETR_PIN  = 17
CMP_OUT_PIN       = 4

GPIO.setup(POTENTIOMETR_PIN, GPIO.OUT)
GPIO.setup(DAC_PIN_LIST, GPIO.OUT)
GPIO.setup(CMP_OUT_PIN, GPIO.IN)

DIODS_PIN_LIST = [21, 20, 16, 12,  7,  8, 25, 24]
GPIO.setup(DIODS_PIN_LIST, GPIO.OUT)



def decToBinList(decNumber) :
    result = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range (0, 8) :
        if (decNumber % 2) == 1 :
            result [i] = 1+-
        decNumber = decNumber // 2

        if decNumber == 0 :
            return result
    
    return result

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
GPIO.output(POTENTIOMETR_PIN)
GPIO.cleanup()