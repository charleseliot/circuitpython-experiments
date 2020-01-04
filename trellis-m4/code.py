import time
import adafruit_trellism4
import board
import busio as io
import adafruit_ds3231

trellis = adafruit_trellism4.TrellisM4Express()

i2c = io.I2C(board.SCL, board.SDA)
rtc = adafruit_ds3231.DS3231(i2c)

ZERO_COLOR = (10, 10, 10)
ONE_COLOR = (128, 0, 0)
BLACK = (0, 0, 0)

INITIAL_TIME = (2000, 1, 1, 0, 0, 0, 5, 1, -1)

def writeBcdDigitToColumn(val, col):
    for row in range(3, -1, -1):
        if (val % 2 == 1):
            trellis.pixels[(col, row)] = ONE_COLOR
        else:
            trellis.pixels[(col, row)] = ZERO_COLOR
        val = val // 2

def initializeTrellis():
    trellis.pixels.brightness = 0.5

    red = 0
    blue = 0
    green = 0

    for row in range(4):
        for col in range(8):
            trellis.pixels[(col, row)] = (red, green, blue)
            blue = blue + 3

def displayBcdTime(t):
        secondsValue = t.tm_sec
        secondsValueLowDigit = secondsValue % 10
        secondsValueHighDigit = secondsValue // 10

        minutesValue = t.tm_min
        minutesValueLowDigit = minutesValue % 10
        minutesValueHighDigit = minutesValue // 10

        hoursValue = t.tm_hour
        hoursValueLowDigit = hoursValue % 10
        hoursValueHighDigit = hoursValue // 10

        writeBcdDigitToColumn(hoursValueHighDigit, 0)
        writeBcdDigitToColumn(hoursValueLowDigit, 1)
        writeBcdDigitToColumn(minutesValueHighDigit, 3)
        writeBcdDigitToColumn(minutesValueLowDigit, 4)
        writeBcdDigitToColumn(secondsValueHighDigit, 6)
        writeBcdDigitToColumn(secondsValueLowDigit, 7)

initializeTrellis()

clock = INITIAL_TIME

while True:
    t = rtc.datetime

    if (t != clock):
        clock = t
        displayBcdTime(t)

    time.sleep(0.2)
