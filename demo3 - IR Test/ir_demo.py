import board
from digitalio import DigitalInOut, Direction
from microcontroller import delay_us

IR = DigitalInOut(board.GP28)
IR.direction = Direction.INPUT

def getkey():
    global IR
    if not IR.value:
        count = 0
        while ((IR.value == 0) and (count < 100)): #9ms
            count += 1
            delay_us(100)
        if(count < 10):
            return None
        count = 0
        while ((IR.value == 1) and (count < 50)): #4.5ms
            count += 1
            delay_us(100)

        idx = 0
        cnt = 0
        data = [0,0,0,0]
        for i in range(0,32):
            count = 0
            while ((IR.value == 0) and (count < 10)):    #0.56ms
                count += 1
                delay_us(100)

            count = 0
            while ((IR.value == 1) and (count < 20)):   #0: 0.56mx
                count += 1                                #1: 1.69ms
                delay_us(100)

            if count > 7:
                data[idx] |= 1<<cnt
            if cnt == 7:
                cnt = 0
                idx += 1
            else:
                cnt += 1

        if data[0]+data[1] == 0xFF and data[2]+data[3] == 0xFF:  #check
            return data[2]
        else:
            return("repeat")
while True:
    key = getkey()
    if(key != None):
        if key != "repeat":
            print(hex(key))
        else:
            print(key)
