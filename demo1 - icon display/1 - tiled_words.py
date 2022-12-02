# Minimal example displaying an image tiled across multiple RGB LED matrices.
# This is written for MatrixPortal and four 64x32 pixel matrices, but could
# be adapted to different boards and matrix combinations.
# No additional libraries required, just uses displayio.
# Image word.bmp should be in CIRCUITPY images directory.

import board
import displayio
import framebufferio
import rgbmatrix
from digitalio import DigitalInOut, Direction

bit_depth_value = 6
base_width = 64
base_height = 32
chain_across = 1
tile_down = 1
serpentine_value = True

width_value = base_width * chain_across
height_value = base_height * tile_down

displayio.release_displays() # Release current display, we'll create our own

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


# Create RGB matrix object for a chain of four 64x32 matrices tiled into
# a single 128x64 pixel display -- two matrices across, two down, with the
# second row being flipped. width and height args are the combined size of
# all the tiled sub-matrices. tile arg is the number of rows of matrices in
# the chain (horizontal tiling is implicit from the width argument, doesn't
# need to be specified, but vertical tiling must be explicitly stated).
# The serpentine argument indicates whether alternate rows are flipped --
# cabling is easier this way, downside is colors may be slightly different
# when viewed off-angle. bit_depth and pins are same as other examples.
matrix = rgbmatrix.RGBMatrix(
    width=width_value, height=height_value, bit_depth=bit_depth_value,
    rgb_pins=[board.GP2, board.GP3, board.GP4, board.GP5, board.GP8, board.GP9],
    addr_pins=[board.GP10, board.GP16, board.GP18, board.GP20],
    clock_pin=board.GP11, latch_pin=board.GP12, output_enable_pin=board.GP13,
    tile=tile_down, serpentine=serpentine_value,
    doublebuffer=True)

# Associate matrix with a Display to use displayio features
DISPLAY = framebufferio.FramebufferDisplay(matrix, auto_refresh=False,
                                           rotation=180)

# Load BMP image, create Group and TileGrid to hold it
BITMAP = displayio.OnDiskBitmap(open('images/Word.bmp', 'rb'))
GROUP = displayio.Group()
GROUP.append(displayio.TileGrid(
    BITMAP,
    pixel_shader=getattr(BITMAP, 'pixel_shader', displayio.ColorConverter()),
    width=1,
    height=1,
    tile_width=BITMAP.width,
    tile_height=BITMAP.height))
DISPLAY.show(GROUP)
DISPLAY.refresh()

# Nothing interactive, just hold the image there
while True:
    pass

