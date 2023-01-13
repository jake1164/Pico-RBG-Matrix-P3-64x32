# This example implements a simple two line scroller using
# Adafruit_CircuitPython_Display_Text. Each line has its own color
# and it is possible to modify the example to use other fonts and non-standard
# characters.

import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time
import displaySubsystem
import keyInput
from driver_buzzer import *
from driver_lightSensor import *

MaxDays = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

KEY_MENU = 0
KEY_DOWN = 1
KEY_UP = 2

beepFlag = 1
startBeepFlag = 0
beepCount = 0

autoLightFlag = 0
timeFormatFlag = 0 # 12 or 24 (0 or 1) hour display.

selectSettingOptions = 0
pageID = 0

timeSettingLabel = 0
timeTemp = [0, 0, 0]  # hour,min,sec
dateTemp = [0, 0, 0]  # year,mon,mday

keyMenuValue = 0
keyDownValue = 0
keyUpValue = 0

# Lookup table for names of days (nicer printing).

bit_depth_value = 1
base_width = 64
base_height = 32
chain_across = 1
tile_down = 2
serpentine_value = True

width_value = base_width * chain_across
height_value = base_height * tile_down


# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()

# send register
R1 = DigitalInOut(board.GP2)
G1 = DigitalInOut(board.GP3)
B1 = DigitalInOut(board.GP4)
R2 = DigitalInOut(board.GP5)
G2 = DigitalInOut(board.GP8)
B2 = DigitalInOut(board.GP9)
CLK = DigitalInOut(board.GP11)
STB = DigitalInOut(board.GP12)
OE = DigitalInOut(board.GP13)

R1.direction = Direction.OUTPUT
G1.direction = Direction.OUTPUT
B1.direction = Direction.OUTPUT
R2.direction = Direction.OUTPUT
G2.direction = Direction.OUTPUT
B2.direction = Direction.OUTPUT
CLK.direction = Direction.OUTPUT
STB.direction = Direction.OUTPUT
OE.direction = Direction.OUTPUT

OE.value = True
STB.value = False
CLK.value = False

MaxLed = 64

c12 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
c13 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c12[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 12):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

for l in range(0, MaxLed):
    y = l % 16
    R1.value = False
    G1.value = False
    B1.value = False
    R2.value = False
    G2.value = False
    B2.value = False

    if c13[y] == 1:
        R1.value = True
        G1.value = True
        B1.value = True
        R2.value = True
        G2.value = True
        B2.value = True
    if l > (MaxLed - 13):
        STB.value = True
    else:
        STB.value = False
    CLK.value = True
    # time.sleep(0.000002)
    CLK.value = False
STB.value = False
CLK.value = False

R1.deinit()
G1.deinit()
B1.deinit()
R2.deinit()
G2.deinit()
B2.deinit()
CLK.deinit()
STB.deinit()
OE.deinit()

# This next call creates the RGB Matrix object itself. It has the given width
# and height. bit_depth can range from 1 to 6; higher numbers allow more color
# shades to be displayed, but increase memory usage and slow down your Python
# code. If you just want to show primary colors plus black and white, use 1.
# Otherwise, try 3, 4 and 5 to see which effect you like best.
#
# These lines are for the Feather M4 Express. If you're using a different board,
# check the guide to find the pins and wiring diagrams for your board.
# If you have a matrix with a different width or height, change that too.
# If you have a 16x32 display, try with just a single line of text.

matrix = rgbmatrix.RGBMatrix(
    width=width_value,height=height_value,bit_depth=bit_depth_value,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11,latch_pin=board.GP12,output_enable_pin=board.GP13,
    tile=tile_down,serpentine=serpentine_value,
    doublebuffer=True,
)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)
display.rotation = 180


line1 = adafruit_display_text.label.Label(terminalio.FONT, color=0x00DD00)


line2 = adafruit_display_text.label.Label(terminalio.FONT, color=0x00DDDD)


line3 = adafruit_display_text.label.Label(terminalio.FONT, color=0x0000DD)
line3.x = 12
line3.y = 56

# Put each line of text into a Group, then show that group.
g = displayio.Group()
g.append(line1)
g.append(line2)
g.append(line3)
display.show(g)

keyInput.keyInit()

showSystem = displaySubsystem.DISPLAYSUBSYSTEM(timeFormatFlag)


def checkLightSensor():
    if autoLightFlag == 1:
        lightSensorValue = get_voltage()
        if lightSensorValue > 2800:
            display.brightness = 0.0
        else:
            display.brightness = 0.1


def judgmentBuzzerSwitch():
    global startBeepFlag
    if beepFlag == 1 and startBeepFlag == 0:
        BUZZERON()
        startBeepFlag = 1


def isLeapYear(year):
    if year % 4 == 0 and year % 100 != 0:
        return True
    if year % 400 == 0:
        return True
    return False


def getMaxDay(month, year):
    if month < 1 or month > 12:
        print("error month")
        return -1
    maxDay = MaxDays[month]
    if year != -1 and month == 2:
        if isLeapYear(year):
            maxDay += 1
    return maxDay


def keyMenuProcessingFunction():
    global pageID, timeSettingLabel
    if pageID == 2 and selectSettingOptions <= 1:
        timeSettingLabel += 1
        if timeSettingLabel > 2:
            timeSettingLabel = 0
    pageID += 1
    if pageID > 2:
        pageID = 2


def keyDownProcessingFunction():
    global selectSettingOptions, timeTemp, dateTemp, beepFlag, autoLightFlag, timeFormatFlag
    if pageID == 1:
        selectSettingOptions -= 1
        if selectSettingOptions == -1:
            selectSettingOptions = 4
    if pageID == 2:
        if selectSettingOptions == 0:
            if timeSettingLabel == 0:
                timeTemp[0] -= 1
                if timeTemp[0] < 0:
                    timeTemp[0] = 23
            elif timeSettingLabel == 1:
                timeTemp[1] -= 1
                if timeTemp[1] < 0:
                    timeTemp[1] = 59
            else:
                timeTemp[2] -= 1
                if timeTemp[2] < 0:
                    timeTemp[2] = 59
        if selectSettingOptions == 1:
            if timeSettingLabel == 0:
                dateTemp[0] -= 1
                if dateTemp[0] < 2000:
                    dateTemp[0] = 2099
            elif timeSettingLabel == 1:
                dateTemp[1] -= 1
                if dateTemp[1] < 1:
                    dateTemp[1] = 12
            else:
                dateTemp[2] -= 1
                if dateTemp[2] < 1:
                    dateTemp[2] = getMaxDay(dateTemp[1], dateTemp[0])
        if selectSettingOptions == 2:
            if beepFlag:
                beepFlag = 0
            else:
                beepFlag = 1
        if selectSettingOptions == 3:
            if autoLightFlag:
                autoLightFlag = 0
            else:
                autoLightFlag = 1
        if selectSettingOptions == 4:
            if timeFormatFlag:
                timeFormatFlag = 0 # 12 hour
            else:
                timeFormatFlag = 1 # 24 hour
            showSystem.setTimeFormat(timeFormatFlag)


def keyUpProcessingFunction():
    global selectSettingOptions, timeTemp, dateTemp, beepFlag, autoLightFlag, timeFormatFlag
    if pageID == 1:
        selectSettingOptions += 1
        if selectSettingOptions == 5:
            selectSettingOptions = 0
    if pageID == 2:
        if selectSettingOptions == 0:
            if timeSettingLabel == 0:
                timeTemp[0] += 1
                if timeTemp[0] == 24:
                    timeTemp[0] = 0
            elif timeSettingLabel == 1:
                timeTemp[1] += 1
                if timeTemp[1] == 60:
                    timeTemp[1] = 0
            else:
                timeTemp[2] += 1
                if timeTemp[2] == 60:
                    timeTemp[2] = 0
        if selectSettingOptions == 1:
            if timeSettingLabel == 0:
                dateTemp[0] += 1
                if dateTemp[0] > 2099:
                    dateTemp[0] = 2000
            elif timeSettingLabel == 1:
                dateTemp[1] += 1
                if dateTemp[1] > 12:
                    dateTemp[1] = 1
            else:
                dateTemp[2] += 1
                if dateTemp[2] > getMaxDay(dateTemp[1], dateTemp[0]):
                    dateTemp[2] = 1
        if selectSettingOptions == 2:
            if beepFlag:
                beepFlag = 0
            else:
                beepFlag = 1
        if selectSettingOptions == 3:
            if autoLightFlag:
                autoLightFlag = 0
            else:
                autoLightFlag = 1
        if selectSettingOptions == 4:
            if timeFormatFlag:
                timeFormatFlag = 0 # 12 hour
            else:
                timeFormatFlag = 1 # 24 hour
            showSystem.setTimeFormat(timeFormatFlag)
            
            


def keyExitProcessingFunction():
    global pageID, timeSettingLabel
    if pageID == 2 and selectSettingOptions <= 1: 
        showSystem.setDateTime(selectSettingOptions, dateTemp, timeTemp)
        timeSettingLabel = 0
    pageID -= 1
    if pageID < 0:
        pageID = 0


def keyProcessing(keyValue):
    global keyMenuValue, keyDownValue, keyUpValue, beepCount, startBeepFlag
    if keyValue == KEY_MENU:  
        keyMenuValue += 1
    if keyValue == KEY_DOWN:
        keyDownValue += 1
    if keyValue == KEY_UP:
        keyUpValue += 1

    if startBeepFlag == 1:
        beepCount += 1
        if beepCount == 3:
            BUZZEROFF()
            beepCount = 0
            startBeepFlag = 0

    if keyMenuValue > 0 and keyMenuValue < 20 and keyValue == None:
        keyMenuProcessingFunction()
        judgmentBuzzerSwitch()
        keyMenuValue = 0
    elif keyMenuValue >= 20 and keyValue == None:
        keyMenuValue = 0

    if keyDownValue > 0 and keyDownValue < 20 and keyValue == None:
        keyDownProcessingFunction()
        judgmentBuzzerSwitch()
        keyDownValue = 0
    elif keyDownValue >= 20 and keyValue == None:
        keyDownValue = 0

    if keyUpValue > 0 and keyUpValue < 20 and keyValue == None:
        keyUpProcessingFunction()
        judgmentBuzzerSwitch()
        keyUpValue = 0
    elif keyUpValue >= 20 and keyValue == None:
        keyExitProcessingFunction()
        judgmentBuzzerSwitch()
        keyUpValue = 0


# matrix.deinit()

while True:
    checkLightSensor()
    key_value = keyInput.getKeyValue()
    keyProcessing(key_value)
    if pageID == 0:
        showSystem.showDateTimePage(line1, line2, line3)
    if pageID == 1:
        line3.text = ""
        showSystem.showSetListPage(line1, line2, selectSettingOptions)
    if pageID == 2 and selectSettingOptions == 0:
        line1.text = ""
        showSystem.timeSettingPage(line2, line3, timeSettingLabel, timeTemp)
    if pageID == 2 and selectSettingOptions == 1:
        line1.text = ""
        showSystem.dateSettingPage(line2, line3, timeSettingLabel, dateTemp)
    if pageID == 2 and selectSettingOptions > 1:
        line1.text = ""
        showSystem.onOffPage(
            line2, line3, selectSettingOptions, beepFlag, autoLightFlag, timeFormatFlag
        )
