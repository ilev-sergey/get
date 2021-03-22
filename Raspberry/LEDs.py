import RPi.GPIO as GPIO
import time


def convert(num):
    a = [21, 20, 16, 12, 7, 8, 25, 24]
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
        if reversed_binary[1]:
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
