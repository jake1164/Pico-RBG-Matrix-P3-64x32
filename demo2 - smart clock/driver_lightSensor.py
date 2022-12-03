import board
from analogio import AnalogIn

analog_in = AnalogIn(board.GP26)


def get_voltage():
    return int((analog_in.value * 3300) / 65536)