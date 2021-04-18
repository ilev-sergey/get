import RPi.GPIO as GPIO


def dec_to_bin_list(a):  # return binary list of number
    return list(bin(a)[2::].zfill(8))


def convert(number):  # convert number of LED to number on board
    a = [26, 19, 13, 6, 5, 11, 9, 10]
    return a[-number - 1]


def light_up_bin(number):  # light up binary equivalent to number
    for i in range(8):
        GPIO.setup(convert(i), GPIO.OUT)
        GPIO.output(convert(i), dec_to_bin_list(number)[i])


print("Enter value (-1 to exit) > 25")
while True:
    value = int(input())
    if value == -1:
        GPIO.cleanup()
        exit()
    elif value > 255 or value <= 25:
        print("Wrong number")
    else:
        voltage = value / 25 * 0.32
        print("{} = {}V".format(value, round(voltage, 4)))

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        light_up_bin(value)
