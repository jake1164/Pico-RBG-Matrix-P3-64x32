import board
import time
from analogio import AnalogIn
import displayio
import rgbmatrix
import framebufferio
import terminalio
from adafruit_display_text.label import Label

analog_in = AnalogIn(board.GP26)

bit_depth_value = 1
base_width = 64
base_height = 32
chain_across = 1
tile_down = 1
serpentine_value = True

width_value = base_width * chain_across
height_value = base_height * tile_down

displayio.release_displays() # Release current display, we'll create our own

def get_voltage():
    """ returns the voltage of the light sensor """
    return int((analog_in.value * 3300) / 65536)

matrix = rgbmatrix.RGBMatrix(
    width=width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile=tile_down, serpentine=serpentine_value,
    doublebuffer=True)

# Associate matrix with a Display to use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)
display.rotation = 0

group = displayio.Group()

line1 = Label(
    terminalio.FONT,
    color=0xff0000,
    text="Brightness")
line1.x = 2
line1.y = 8
group.append(line1)

line2 = Label(
    terminalio.FONT,
    color=0x0080ff,
    text="0000")
line2.x = 8
line2.y = 24
group.append(line2)

display.show(group)

while True:
    v_string = str(get_voltage())
    
    pos = 10
    if len(v_string) > 0:
        pos = int(width_value / len(v_string))
    line2.text = v_string

    line2.x = pos
    display.show(group)     
    time.sleep(3)