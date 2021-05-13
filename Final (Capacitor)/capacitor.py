import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

import time
import numpy as np


TM_Pin  = 17
CMP_Pin = 4

DAC     = (26, 19, 13,  6, 5, 11,  9, 10)
GPIO    = (21, 20, 16, 12, 7,  8, 25, 24)

MAX_VOLTAGE = 3.3

def num2pins(pins, value):
    for i in range(7, -1, -1):
        GPIO.output(pins[i], value % 2)
        value //= 2 # деление без остатка
	#print(value)



def adc():
    start_val = 0
	end_val = 255
    
	while start_val <= end_val:
        
		mid_val = (start_val + end_val) // 2 # деление без остатка
        num2pins(DAC, mid_val)
        time.sleep(0.0005)

        if GPIO.input(CMP_Pin) == 0:
            end_val = mid_val - 1
        else:
            start_val = mid_val + 1
    
    if end_val < 0:
        return start_val
    else:
        return end_val


def get_analog_volt(digital_voltage):
	analog_volt = MAX_VOLTAGE * digital_voltage / 255
    return analog_volt


def GPIO_prepate():
	GPIO.setmode(GPIO.BCM)
    GPIO.setup(TM_Pin, GPIO.OUT)
    GPIO.setup(CMP_Pin, GPIO.IN)
    GPIO.setup(DAC, GPIO.OUT)
    GPIO.setup(GPIO, GPIO.OUT)

try:

	GPIO_prepare() 				# Подготовка пинов и т.п.

    measure = [] 				# Массив напряжений
    times_massive = []			# Массив времени
    digital_voltage = 0			# Начальное (цифровое) напряжение

    GPIO.output(TM_Pin, 0)		# эта строчка не нужна!!!	
    time.sleep(0.1)				

    START_TIME = time.time() 	# Время начала измерений
    GPIO.output(TM_Pin, 1)		# подача питания на troykaModule и начало зарядки конденсатора через резистор

    while digital_voltage < 250: 							# Пока (цифровое) напряжение не достигло почти максимума
        digital_voltage = adc()								# непрерывное измерение напряжения на конденсаторе в
        measure.append(get_analog_volt(digital_voltage))	# процессе заряда при помощи функции adc() до момента его почти полной зарядки
        times_massive.append(time.time() - START_TIME)
        time.sleep(0.002)

    GPIO.output(TM_Pin, 0)		# отключение питания troykaModule и начало разрядки конденсатора через резистор

    while digital_voltage > 5: 		# непрерывное измерение напряжения на конденсаторе в процессе его разрядки
        digital_voltage = adc()		# при помощи функции adc() до момента его почти полной разрядки
        measure.append(get_analog_volt(digital_voltage))	# сохранение измеренных кодов напряжений в список measure
        times_massive.append(time.time() - START_TIME)		# сохранение измеренных времен в список times_massive
        time.sleep(0.002)

    np.savetxt('data.txt', measure, fmt='%d') # '%d %d'		# сохранение полученных измерений файл data.txt при помощи функции np.savetxt('data.txt', measure, fmt='%d') модуля numpy


    # На отл 9 
    dT = 0

    for i in range(1, len(measure)):
        dT += times_massive[i] - times_massive[i-1]

    dT /= len(times_massive) - 1
    dV = MAX_VOLTAGE / 255

    with open("settings.txt", "w") as settings:
        settings.write(str(dT)+"\n"+str(dV))

    # На отл 10

    plt.plot(times_massive, measure)		# отображение графика полученных измерений при помощи
											# функции plt.plot(measure) модуля matplotlib.pyplot;

    plt.title('U(t)')

    plt.ylabel('Напряжение, В')
    plt.xlabel('Время, с')
    
	plt.show()


finally:

    GPIO.cleanup()



