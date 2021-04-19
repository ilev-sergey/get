import RPi.GPIO as GPIO
import time


def dec_to_bin_list(a):  # return binary list of number
    return list(map(int, (list(bin(a)[2::].zfill(8)))))


def convert(number):  # convert number of LED to number on board
    a = [26, 19, 13, 6, 5, 11, 9, 10]
    return a[-number - 1]


def light_up_bin(number):  # light up binary equivalent to number
    for i in range(8):
        GPIO.setup([26, 19, 13, 6, 5, 11, 9, 10], GPIO.OUT)
        GPIO.output([26, 19, 13, 6, 5, 11, 9, 10], dec_to_bin_list(number))


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, 1)
prev = 0
while True:
    GPIO.setup(4, GPIO.IN)
    initial_state = GPIO.input(4)
    for value in range(26, 256):
        light_up_bin(value)
        time.sleep(0.01)
        current_state = GPIO.input(4)
        if current_state != 1:
            voltage = value / 25 * 0.32
            if voltage == prev:
                break
            prev = voltage
            print("Digital value: {}, Analog value: {} V".format(value, round(voltage, 4)))
            time.sleep(1)
            break
