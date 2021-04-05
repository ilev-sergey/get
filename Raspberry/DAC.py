import RPi.GPIO as GPIO
import time
import numpy as np
import matplotlib.pyplot as plt


def convert(num):
    a = [26, 19, 13, 6, 5, 11, 9, 10]
    return a[-num - 1]


def light_up(num):
    num = convert(num)
    GPIO.setup(num, GPIO.OUT)
    GPIO.output(num, 1)


def light_down(num):
    num = convert(num)
    GPIO.setup(num, GPIO.OUT)
    GPIO.output(num, 0)


def flash_up(num, period):
    num = convert(num)
    GPIO.setup(num, GPIO.OUT)
    GPIO.output(num, 1)
    time.sleep(period)
    GPIO.output(num, 0)


def flash_down(num, period):
    num = convert(num)
    GPIO.setup(num, GPIO.OUT)
    GPIO.output(num, 0)
    time.sleep(period)
    GPIO.output(num, 1)


def blink(num, count, period):
    for _ in range(count):
        flash_up(num, period)
        time.sleep(period)


def running_light(count, period):
    for _ in range(count):
        for k in range(8):
            flash_up(k, period)


def running_dark(count, period):
    for i in range(8):
        light_up(i)
    for _ in range(count):
        for k in range(8):
            flash_down(k, period)
    for i in range(8):
        light_down(i)


def dec_to_bin_list(number):
    binary = bin(number)[2::].zfill(8)
    return list(map(int, list(binary)))


def light_binary(binary, period):
    reversed_binary = list(reversed(binary))
    for i in range(len(reversed_binary)):
        if reversed_binary[i]:
            light_up(i)
    time.sleep(period)
    for i in range(len(reversed_binary)):
        if reversed_binary[i]:
            light_down(i)
            
def dark_binary(binary, period):
    reversed_binary = list(reversed(binary))
    for i in range(len(reversed_binary)):
        if reversed_binary[i]:
            light_down(i)
    time.sleep(period)
    for i in range(len(reversed_binary)):
        if reversed_binary[i]:
            light_up(i)
            
def light_binary_unstop(binary):
    reversed_binary = list(reversed(binary))
    for i in range(len(reversed_binary)):
        if reversed_binary[i]:
            light_up(i)
    tmp = input()
    if tmp == "exit":
        for i in range(len(reversed_binary)):
            if reversed_binary[i]:
                light_down(i)


def shift(a, step):
    if step > 0:
        a.insert(0, a.pop())
    if step < 0:
        a.append(a.pop(0))
    return a


def running_pattern(number, direction, period):
    binary = dec_to_bin_list(number)
    light_binary(binary, period)
    for i in range(abs(direction)):
        if direction > 0:
            shift(binary, 1)
            light_binary(binary, period)
        if direction < 0:
            shift(binary, -1)
            light_binary(binary, period)
    return binary


def PWM(num, frequency):
    GPIO.setup(num, GPIO.OUT)
    p = GPIO.PWM(num, frequency)
    p.start(0)
    try:
        while True:
            for dc in range(0, 101, 5):
                p.ChangeDutyCycle(dc)
                time.sleep(0.1)
            for dc in range(100, -1, -5):
                p.ChangeDutyCycle(dc)
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    p.stop()
    GPIO.cleanup()
    


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

try:
    name_of_def = input().split()
    while True:
        if name_of_def[0] == "num2dac":
            print("Введите число")
            tmp = input().split()
            GPIO.setmode(GPIO.BCM)
            light_binary_unstop(dec_to_bin_list(int(tmp[0])))
        elif name_of_def[0] == "repeat":
            print("Введите количество повторений")
            tmp = int(input())
            GPIO.setmode(GPIO.BCM)
            for i in range(tmp):
                for k in range(256):
                    light_binary(dec_to_bin_list(k), 0.01)
                for m in range(255, -1, -1):
                    light_binary(dec_to_bin_list(m), 0.01)
        elif name_of_def[0] == "sin":
            GPIO.setmode(GPIO.BCM)
            frequency = float(input())
            samplingFrequency = float(input())
            timing = float(input())
            times = np.arange(0, timing, 1/frequency)
            amplitude = 256 * np.sin(times)
            plt.plot(times, amplitude)
            plt.title("Синус")
            plt.xlabel("Время")
            plt.ylabel("Амплитуда")
            plt.show()
            for i in range(len(times)):
                light_binary(dec_to_bin_list(round(amplitude[i])), 1/samplingFrequency)
        elif name_of_def[0] == "music":
            print("NO")
        elif name_of_def[0] == "exit":
            GPIO.cleanup()
            exit()
except Exception:
    print("Fail")
    exit()
finally:
    GPIO.cleanup()