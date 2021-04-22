import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

DAC_PIN_LIST      = [26, 19, 13,  6,  5, 11,  9, 10]
POTENTIOMETR_PIN  = 17
CMP_OUT_PIN       = 4

GPIO.setup(POTENTIOMETR_PIN, GPIO.OUT)
GPIO.setup(DAC_PIN_LIST, GPIO.OUT)
GPIO.setup(CMP_OUT_PIN, GPIO.IN)


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
    GPIO.output(DAC_PIN_LIST, 0)

    for i in range (0, 8) :
        if result[i] == 1 :
            GPIO.output(DAC_PIN_LIST[7 - i], 1)


def search() :
    volt = 0

    for i in range (0, 255) :
        num2dac(i)
        time.sleep(0.0005)
        if GPIO.input(CMP_OUT_PIN) != 1 :
            volt = 3.3 * float (i) / 255
            break
    
    return volt


def binSearch() :
    value = 0
    i     = 128

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
    return 3.3 * float (value) / 255



GPIO.output(POTENTIOMETR_PIN, 1)

lastVolt = 0
NewVolt = 0

while True:    
    NewVolt = binSearch()

    if abs(NewVolt - lastVolt) > 1.0 / 255.0 :
        print(NewVolt, int (NewVolt * 255 / 3.3))
        lastVolt = NewVolt



GPIO.output(DAC_PIN_LIST, 0)
GPIO.output(POTENTIOMETR_PIN)
GPIO.cleanup()