import board
from digitalio import DigitalInOut, Direction

buzzer = DigitalInOut(board.GP27)
buzzer.direction = Direction.OUTPUT

def BUZZERON():
    buzzer.value = True
def BUZZEROFF():
    buzzer.value = False