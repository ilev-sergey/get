import RPi.GPIO as GPIO
import time
import matplotlib.pyplot as plt


def dec_to_bin_list(a):  # return binary list of number
    return list(map(int, (list(bin(a)[2::].zfill(8)))))


def light_up_bin(number):  # light up binary equivalent to number
    GPIO.setup([26, 19, 13, 6, 5, 11, 9, 10], GPIO.OUT)
    GPIO.output([26, 19, 13, 6, 5, 11, 9, 10], dec_to_bin_list(number))
        
        
GPIO.cleanup()
prev = 0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup([26, 19, 13, 6, 5, 11, 9, 10], GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, 1)
while True:
    a = 0
    b = 256
    value = 128
    tmp = "a"
    first = True
    while True:
        GPIO.setup(4, GPIO.IN)
        initial_state = GPIO.input(4)
        light_up_bin(value)
        time.sleep(0.001)
        current_state = GPIO.input(4)
        if (current_state != initial_state and tmp == "a") or \
                (current_state == initial_state and tmp == "b") or (first and current_state == 0):
            b = (a + b) // 2
            tmp = "b"
        else:
            a = (a + b) // 2
            tmp = "a"
        value = (a + b) // 2
        first = False
        if b - a == 1:
            voltage = value / 25 * 0.32
            prev = voltage
            if value != 0:
                print("Digital value: {}, Analog value: {} V".format(value, round(voltage, 4)))
            break